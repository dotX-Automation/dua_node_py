"""
DUA ROS 2 node base class implementation.

dotX Automation s.r.l. <info@dotxautomation.com>

May 8, 2025
"""

# Copyright 2025 dotX Automation s.r.l.
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


from rclpy.node import Node

from rclpy.qos import QoSProfile
import dua_qos_py.dua_qos_reliable as dua_qos_reliable

from params_manager_py.params_manager import PManager

from rclpy.callback_groups import CallbackGroup, ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup

from rclpy.timer import Timer

from rclpy.subscription import Subscription
from rclpy.publisher import Publisher

from rclpy.service import Service
from simple_serviceclient_py.simple_serviceclient import Client

from rclpy.action import ActionServer
from simple_actionclient_py.simple_actionclient import Client as ActionClient

from typing import Any, Callable


class NodeBase(Node):
    """
    Extends rclpy.node.Node adding features from DUA packages.
    """

    def __init__(self, node_name: str, verbose: bool = False) -> None:
        """
        Constructor.

        :param node_name: Name of the node.
        :param verbose: Verbosity flag.
        """
        super().__init__(node_name)

        self._verbose = verbose
        self.pmanager = PManager(self, verbose)

        # This is possible thanks to Python's Method Resolution Order (MRO)
        self._dua_init_node()

    def _dua_init_node(self):
        """
        Initializes the node calling internal initializers.
        """
        self._dua_init_parameters()
        self._dua_init_cgroups()
        self._dua_init_timers()
        self._dua_init_subscribers()
        self._dua_init_publishers()
        self._dua_init_service_servers()
        self._dua_init_service_clients()
        self._dua_init_action_servers()
        self._dua_init_action_clients()

    def _dua_init_parameters(self):
        """
        Initializes node parameters.
        """
        if self._verbose:
            self.get_logger().info("--- PARAMETERS ---")
        self.pmanager.init()
        self.init_parameters()

    def _dua_init_cgroups(self):
        """
        Initializes callback groups.
        """
        self.init_cgroups()

    def _dua_init_timers(self):
        """
        Initializes timers.
        """
        if self._verbose:
            self.get_logger().info("--- TIMERS ---")
        self.init_timers()

    def _dua_init_subscribers(self):
        """
        Initializes subscribers.
        """
        if self._verbose:
            self.get_logger().info("--- SUBSCRIBERS ---")
        self.init_subscribers()

    def _dua_init_publishers(self):
        """
        Initializes publishers.
        """
        if self._verbose:
            self.get_logger().info("--- PUBLISHERS ---")
        self.init_publishers()

    def _dua_init_service_servers(self):
        """
        Initializes service servers.
        """
        if self._verbose:
            self.get_logger().info("--- SERVICE SERVERS ---")
        self.init_service_servers()

    def _dua_init_service_clients(self):
        """
        Initializes service clients.
        """
        if self._verbose:
            self.get_logger().info("--- SERVICE CLIENTS ---")
        self.init_service_clients()

    def _dua_init_action_servers(self):
        """
        Initializes action servers.
        """
        if self._verbose:
            self.get_logger().info("--- ACTION SERVERS ---")
        self.init_action_servers()

    def _dua_init_action_clients(self):
        """
        Initializes action clients.
        """
        if self._verbose:
            self.get_logger().info("--- ACTION CLIENTS ---")
        self.init_action_clients()

    def dua_create_exclusive_cgroup(self) -> CallbackGroup:
        """
        Returns a mutually exclusive callback group.

        :return: Callback group.
        """
        return MutuallyExclusiveCallbackGroup()

    def dua_create_reentrant_cgroup(self) -> CallbackGroup:
        """
        Returns a reentrant callback group.

        :return: Callback group.
        """
        return ReentrantCallbackGroup()

    def dua_create_timer(
        self,
        name: str,
        period: int,
        callback: Callable,
        timer_cgroup: CallbackGroup = None
    ) -> Timer:
        """
        Wraps the creation of a timer.

        :param name: Timer name.
        :param period: Timer period [ms].
        :param callback: Timer callback.
        :param timer_cgroup: Timer callback group.
        :return: Timer.
        """
        timer = self.create_timer(
            period / 1000.0,
            callback,
            callback_group=timer_cgroup)
        if self._verbose:
            self.get_logger().info(f"[TIMER] '{name}' ({period} ms)")
        return timer

    def dua_create_subscription(
        self,
        msg_type: Any,
        topic: str,
        callback: Callable,
        qos_profile: QoSProfile = dua_qos_reliable.get_datum_qos(),
        sub_cgroup: CallbackGroup = None
    ) -> Subscription:
        """
        Wraps the creation of a subscriber.

        :param msg_type: Message type.
        :param topic: Topic name.
        :param callback: Subscriber callback.
        :param qos_profile: Quality of Service policy.
        :param sub_cgroup: Subscriber callback group.
        :return: Subscriber.
        """
        subscription = self.create_subscription(
            msg_type=msg_type,
            topic=topic,
            callback=callback,
            qos_profile=qos_profile,
            callback_group=sub_cgroup)
        if self._verbose:
            self.get_logger().info(f"[TOPIC SUB] '{subscription.topic_name}'")
        return subscription

    def dua_create_publisher(
        self,
        msg_type: Any,
        topic: str,
        qos_profile: QoSProfile = dua_qos_reliable.get_datum_qos()
    ) -> Publisher:
        """
        Wraps the creation of a publisher.

        :param msg_type: Message type.
        :param topic: Topic name.
        :param qos_profile: Quality of Service policy.
        :return: Publisher.
        """
        publisher = self.create_publisher(
            msg_type=msg_type,
            topic=topic,
            qos_profile=qos_profile)
        if self._verbose:
            self.get_logger().info(f"[TOPIC PUB] '{publisher.topic_name}'")
        return publisher

    def dua_create_service_server(
        self,
        srv_type: Any,
        srv_name: str,
        callback: Callable,
        srv_cgroup: CallbackGroup = None
    ) -> Service:
        """
        Wraps the creation of a service server.

        :param srv_type: Service type.
        :param srv_name: Service name.
        :param callback: Service callback.
        :param srv_cgroup: Service callback group.
        :return: Service server.
        """
        service = self.create_service(
            srv_type=srv_type,
            srv_name=srv_name,
            callback=callback,
            callback_group=srv_cgroup)
        if self._verbose:
            self.get_logger().info(f"[SERVICE SRV] '{service.service_name}'")
        return service

    def dua_create_service_client(
        self,
        srv_type: Any,
        srv_name: str,
        wait: bool = True
    ) -> Client:
        """
        Wraps the creation of a service client, purposely provided by the simple_serviceclient.Client implementation.

        :param srv_type: Service type.
        :param srv_name: Service name.
        :param wait: Waits for the server to come up.
        :return: Service client.
        """
        client = Client(
            self,
            srv_type,
            srv_name,
            wait)
        if self._verbose:
            self.get_logger().info(f"[SERVICE CLN] '{client.service_name}'")
        return client

    def dua_create_action_server(
        self,
        action_type: Any,
        action_name: str,
        execute_callback: Callable,
        goal_callback: Callable,
        cancel_callback: Callable,
        handle_accepted_callback: Callable,
        as_cgroup: CallbackGroup = None
    ) -> ActionServer:
        """
        Wraps the creation of an action server.

        :param action_type: Action type.
        :param action_name: Action name.
        :param execute_callback: Execute state callback.
        :param goal_callback: New goal reception callback.
        :param cancel_callback: Cancel request callback.
        :param handle_accepted_callback: Accepted state callback.
        :param as_cgroup: Action server callback group.
        :return: Action server.
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
        if self._verbose:
            self.get_logger().info(f"[ACTION SRV] '{self._get_entity_fqn(action_name)}'")
        return server

    def dua_create_action_client(
        self,
        action_type: Any,
        action_name: str,
        feedback_callback: Callable = None,
        wait: bool = True
    ) -> ActionClient:
        """
        Wraps the creation of an action client, purposely provided by the simple_actionclient.Client implementation.

        :param action_type: Action type.
        :param action_name: Action name.
        :param feedback_callback: Feedback message callback.
        :param wait: Waits for the server to come up.
        :return: Action client.
        """
        client = ActionClient(
            self,
            action_type,
            action_name,
            feedback_callback,
            wait)
        if self._verbose:
            self.get_logger().info(f"[ACTION CLN] '{action_name}'")
        return client

    def check_frame_global(self, frame_id: str, frame_prefix: str = "") -> bool:
        """
        Checks if a given frame ID corresponds to the global frame, applying conventions.

        :param frame_id: Frame ID to check.
        :param frame_prefix: Frame prefix to consider (including trailing slash).
        :return: Yes or no.
        """
        return frame_id == frame_prefix + "map" or frame_id == frame_prefix + "world"

    def check_frame_local(self, frame_id: str, frame_prefix: str = "") -> bool:
        """
        Checks if a given frame ID corresponds to the local frame, applying conventions.

        :param frame_id: Frame ID to check.
        :param frame_prefix: Frame prefix to consider (including trailing slash).
        :return: Yes or no.
        """
        return frame_id == frame_prefix + "odom"

    def check_frame_body(self, frame_id: str, frame_prefix: str = "") -> bool:
        """
        Checks if a given frame ID corresponds to the body frame, applying conventions.

        :param frame_id: Frame ID to check.
        :param frame_prefix: Frame prefix to consider (including trailing slash).
        :return: Yes or no.
        """
        return frame_id == frame_prefix + "base_link"

    def _get_entity_fqn(self, entity_name: str) -> str:
        """
        Returns the fully qualified name of an entity.

        :param entity_name: Entity name.
        :return: Fully qualified name.
        """
        ns = self.get_fully_qualified_name()
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
