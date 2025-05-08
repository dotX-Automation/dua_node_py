#
# DUA ROS 2 node base class implementation.
#
# dotX Automation s.r.l. <info@dotxautomation.com>
#
# May 8, 2025
#

#
# Copyright 2024 dotX Automation s.r.l.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.callback_groups import CallbackGroup, ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
from rclpy.timer import Timer
from rclpy.subscription import Subscription
from rclpy.publisher import Publisher
from rclpy.service import Service
from rclpy.client import Client
from rclpy.action import ActionServer, ActionClient
from typing import Any, Callable

import dua_qos_py.dua_qos_reliable as dua_qos_reliable

class NodeBase(Node):
  """
  Extends rclcpp::Node adding features from DUA packages.
  """
  def __init__(self, node_name: str, verbose: bool = False) -> None:
    """
    Constructor.
    Args:
      node_name (str): Name of the node.
      verbose (bool): Verbosity flag.
    """
    super().__init__(node_name)
    # Verbosity flag.
    self.verbose = verbose
    # Parameter manager object.
    self.pmanager = None

    self.dua_init_node()

  def dua_init_node(self):
    """
    Initializes the node calling internal initializers.
    """
    self.dua_init_parameters()
    self.dua_init_cgroups()
    self.dua_init_timers()
    self.dua_init_subscribers()
    self.dua_init_publishers()
    self.dua_init_service_servers()
    self.dua_init_service_clients()
    self.dua_init_action_servers()
    self.dua_init_action_clients()

  def dua_init_parameters(self):
    """
    Initializes node parameters.
    """
    if self.verbose:
      self.get_logger().info("--- PARAMETERS ---")
    self.init_parameters()

  def dua_init_cgroups(self):
    """
    Initializes callback groups.
    """
    self.init_cgroups()

  def dua_init_timers(self):
    """
    Initializes timers.
    """
    if self.verbose:
      self.get_logger().info("--- TIMERS ---")
    self.init_timers()

  def dua_init_subscribers(self):
    """
    Initializes subscribers.
    """
    if self.verbose:
      self.get_logger().info("--- SUBSCRIBERS ---")
    self.init_subscribers()

  def dua_init_publishers(self):
    """
    Initializes publishers.
    """
    if self.verbose:
      self.get_logger().info("--- PUBLISHERS ---")
    self.init_publishers()

  def dua_init_service_servers(self):
    """
    Initializes service servers.
    """
    if self.verbose:
      self.get_logger().info("--- SERVICE SERVERS ---")
    self.init_service_servers()

  def dua_init_service_clients(self):
    """
    Initializes service clients.
    """
    if self.verbose:
      self.get_logger().info("--- SERVICE CLIENTS ---")
    self.init_service_clients()

  def dua_init_action_servers(self):
    """
    Initializes action servers.
    """
    if self.verbose:
      self.get_logger().info("--- ACTION SERVERS ---")
    self.init_action_servers()

  def dua_init_action_clients(self):
    """
    Initializes action clients.
    """
    if self.verbose:
      self.get_logger().info("--- ACTION CLIENTS ---")
    self.init_action_clients()

  def dua_create_exclusive_cgroup(self) -> CallbackGroup:
    """
    Returns a mutually exclusive callback group.
    Returns:
      cgroup (MutuallyExclusiveCallbackGroup).
    """
    cgroup = MutuallyExclusiveCallbackGroup()
    return cgroup

  def dua_create_reentrant_cgroup(self) -> CallbackGroup:
    """
    Returns a reentrant callback group.
    Returns:
      cgroup (ReentrantCallbackGroup).
    """
    cgroup = ReentrantCallbackGroup()
    return cgroup

  def dua_create_timer(self, name: str, period: int, callback: Callable, timer_group: CallbackGroup = None) -> Timer:
    """
    Wraps the creation of a timer.
    Args:
      name (str): Timer name.
      period (int): Timer period [ms].
      callback (Callable): Timer callback.
      timer_cgroup (CallbackGroup): Timer callback group.
    Returns:
      timer (Timer).
    """
    timer = self.create_timer(
      period / 1000.0,
      callback,
      callback_group=timer_group)
    if self.verbose:
      self.get_logger().info(f"[TIMER] '{name}' ({period} ms)")
    return timer

  def dua_create_subscription(self, msg_type: Any, topic: str, callback: Callable, qos_profile: QoSProfile = dua_qos_reliable.get_datum_qos(),
                              sub_cgroup: CallbackGroup = None) -> Subscription:
    """
    Wraps the creation of a subscriber.
    Args:
      msg_type (Any): Message type.
      topic (str): Topic name.
      callback (Callable): Subscriber callback.
      qos_profile (QoSProfile): Quality of Service policy.
      sub_cgroup (CallbackGroup): Subscriber callback group.
    Returns:
      subscription (Subscription).
    """
    subscription = self.create_subscription(
      msg_type=msg_type,
      topic=topic,
      callback=callback,
      qos_profile=qos_profile,
      callback_group=sub_cgroup)
    if self.verbose:
      self.get_logger().info(f"[TOPIC SUB] '{subscription.topic_name}'")
    return subscription

  def dua_create_publisher(self, msg_type: Any, topic: str, qos_profile: QoSProfile = dua_qos_reliable.get_datum_qos()) -> Publisher:
    """
    Wraps the creation of a publisher.
    Args:
      msg_type (Any): Message type.
      topic (str): Topic name.
      qos_profile (QoSProfile): Quality of Service policy.
    Returns:
      publisher (Publisher).
    """
    publisher = self.create_publisher(
      msg_type=msg_type,
      topic=topic,
      qos_profile=qos_profile)
    if self.verbose:
      self.get_logger().info(f"[TOPIC PUB] '{publisher.topic_name}'")
    return publisher

  def dua_create_service_server(self, srv_type: Any, srv_name: str, callback: Callable, srv_cgroup: CallbackGroup = None) -> Service:
    """
    Wraps the creation of a service server.
    Args:
      srv_type (Any): Service type.
      srv_name (str): Service name.
      callback (Callable): Service callback.
      srv_cgroup (CallbackGroup): Service callback group.
    Returns:
      service (Service).
    """
    service = self.create_service(
      srv_type=srv_type,
      srv_name=srv_name,
      callback=callback,
      callback_group=srv_cgroup)
    if self.verbose:
      self.get_logger().info(f"[SERVICE SRV] '{service.service_name}'")
    return service

  def dua_create_service_client(self, srv_type: Any, srv_name: str) -> Client:
    """
    Wraps the creation of a service client.
    Args:
      srv_type (Any): Service type.
      srv_name (str): Service name.
    Returns:
      client (Client).
    """
    client = self.create_client(
      srv_type=srv_type,
      srv_name=srv_name)
    if self.verbose:
      self.get_logger().info(f"[SERVICE CLN] '{client.service_name}'")
    return client

  def dua_create_action_server(self, action_type: Any, action_name: str, execute_callback: Callable, goal_callback: Callable, cancel_callback: Callable,
                            handle_accepted_callback: Callable, as_cgroup: CallbackGroup = None) -> ActionServer:
    """
    Wraps the creation of an action server.
    Args:
      action_type (Any): Action type.
      action_name (str): Action name.
      execute_callback (Callable): Execute callback.
      goal_callback (Callable): Goal callback.
      cancel_callback (Callable): Cancel callback.
      handle_accepted_callback (Callable): Accepted callback.
      as_cgroup (CallbackGroup): Action server callback group.
    Returns:
      server (ActionServer).
    """
    server = ActionServer(
      node=self,
      action_type=action_type,
      action_name=action_name,
      execute_callback=execute_callback,
      goal_callback=goal_callback,
      cancel_callback=cancel_callback,
      handle_accepted_callback=handle_accepted_callback,
      callback_group=as_cgroup)
    if self.verbose:
      self.get_logger().info(f"[ACTION SRV] '{action_name}'")
    return server

  def dua_create_action_client(self, action_type: Any, action_name: str) -> ActionClient:
    """
    Wraps the creation of an action client.
    Args:
      action_type (Any): Action type.
      action_name (str): Action name.
    Returns:
      client (ActionClient).
    """
    client = ActionClient(
      node=self,
      action_type=action_type,
      action_name=action_name)
    if self.verbose:
      self.get_logger().info(f"[ACTION CLN] '{action_name}'")
    return client

  def get_entity_fqn(self, entity_name: str) -> str:
    """
    Returns the fully qualified name of an entity.
    Args:
      entity_name (str): Entity name.
    Returns:
      Fully qualified name, may start with a '~'.
    """
    ns = self.get_namespace()
    pos = entity_name.rfind('/')
    if pos != -1:
      entity_name = entity_name[pos + 1:]
    return f"{ns}/{entity_name}"

  def init_parameters(self) -> None:
    """
    Initializes the node parameters (must be overridden).
    """
    pass

  def init_cgroups(self) -> None:
    """
    Initializes the node callback groups (must be overridden).
    """
    pass

  def init_timers(self) -> None:
    """
    Initializes the node timers (must be overridden).
    """
    pass

  def init_subscribers(self) -> None:
    """
    Initializes the node subscribers (must be overridden).
    """
    pass

  def init_publishers(self) -> None:
    """
    Initializes the node publishers (must be overridden).
    """
    pass

  def init_service_servers(self) -> None:
    """
    Initializes the node service servers (must be overridden).
    """
    pass

  def init_service_clients(self) -> None:
    """
    Initializes the node service clients (must be overridden).
    """
    pass

  def init_action_servers(self) -> None:
    """
    Initializes the node action servers (must be overridden).
    """
    pass

  def init_action_clients(self) -> None:
    """
    Initializes the node action clients (must be overridden).
    """
    pass
