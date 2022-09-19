# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# pylint: disable=protected-access

from typing import Dict, Iterable

from azure.ai.ml._restclient.v2022_10_01_preview import AzureMachineLearningWorkspaces as ServiceClient102022
from azure.ai.ml._restclient.v2022_10_01_preview.models import Registry as RestRegistry
from azure.ai.ml._scope_dependent_operations import OperationsContainer, OperationScope
from azure.ai.ml._telemetry import AML_INTERNAL_LOGGER_NAMESPACE, ActivityType, monitor_with_activity
from azure.ai.ml._utils._logger_utils import OpsLogger
from azure.ai.ml.entities import Registry
from azure.ai.ml.exceptions import ErrorCategory, ErrorTarget, ValidationException
from azure.core.credentials import TokenCredential
from azure.core.polling import LROPoller

ops_logger = OpsLogger(__name__)
logger, module_logger = ops_logger.logger, ops_logger.module_logger


class RegistryOperations:
    """RegistryOperations.

    You should not instantiate this class directly. Instead, you should
    create an MLClient instance that instantiates it for you and
    attaches it as an attribute.
    """

    def __init__(
        self,
        operation_scope: OperationScope,
        service_client: ServiceClient102022,
        all_operations: OperationsContainer,
        credentials: TokenCredential = None,
        **kwargs: Dict,
    ):
        ops_logger.update_info(kwargs)
        self._subscription_id = operation_scope.subscription_id
        self._resource_group_name = operation_scope.resource_group_name
        self._default_registry_name = operation_scope.registry_name
        self._operation = service_client.registries
        self._all_operations = all_operations
        self._credentials = credentials
        self.containerRegistry = "none"
        self._init_kwargs = kwargs

    @monitor_with_activity(logger, "Registry.List", ActivityType.PUBLICAPI)
    def list(self) -> Iterable[Registry]:
        """List all registries that the user has access to in the current
        resource group or subscription.

        :param scope: scope of the listing, "resource_group" or "subscription", defaults to "resource_group"
        :type scope: str, optional
        :return: An iterator like instance of Registry objects
        :rtype: ~azure.core.paging.ItemPaged[Registry]
        """

        return self._operation.list_by_subscription(cls=lambda objs: [Registry._from_rest_object(obj) for obj in objs])

    @monitor_with_activity(logger, "Registry.Get", ActivityType.PUBLICAPI)
    def get(self, name: str = None, **kwargs: Dict) -> Registry:
        """Get a registry by name.

        :param name: Name of the registry.
        :type name: str
        :return: The registry with the provided name.
        :rtype: Registry
        """

        registry_name = self._check_registry_name(name)
        resource_group = self._resource_group_name
        obj = self._operation.get(resource_group, registry_name)
        return Registry._from_rest_object(obj)

    def _check_registry_name(self, name) -> str:
        registry_name = name or self._default_registry_name
        if not registry_name:
            msg = "Please provide a registry name or use a MLClient with a registry name set."
            raise ValidationException(
                message=msg,
                target=ErrorTarget.REGISTRY,
                no_personal_data_message=msg,
                error_category=ErrorCategory.USER_ERROR,
            )
        return registry_name

    @monitor_with_activity(logger, "Registry.BeginCreate", ActivityType.PUBLICAPI)
    def begin_create_or_update(
        self,
        registry: Registry,
        update_dependent_resources: bool = False,
        **kwargs: Dict,
    ) -> LROPoller[RestRegistry]:
        raise NotImplementedError("Placeholder until implemented in subsequent task.")