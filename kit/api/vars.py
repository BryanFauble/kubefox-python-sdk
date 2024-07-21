import re
import os

# Misc
SECRET_MASK = "••••••"
MAX_EVENT_SIZE_BYTES_LIMIT = 16777216  # 16 MiB

t = True
f = False
True_ = t
False_ = f

# Defaults
DEFAULT_LOG_FORMAT = "json"
DEFAULT_LOG_LEVEL = "info"
DEFAULT_MAX_EVENT_SIZE_BYTES = 5242880  # 5 MiB
DEFAULT_RELEASE_ACTIVATION_DEADLINE_SECONDS = 300  # 5 mins
DEFAULT_RELEASE_HISTORY_AGE_LIMIT = 0
DEFAULT_RELEASE_HISTORY_COUNT_LIMIT = 10
DEFAULT_TIMEOUT_SECONDS = 30

# Kubernetes Labels
LABEL_K8S_APP_BRANCH = "kubefox.xigxog.io/app-branch"
LABEL_K8S_APP_COMMIT = "kubefox.xigxog.io/app-commit"
LABEL_K8S_APP_COMMIT_SHORT = "kubefox.xigxog.io/app-commit-short"
LABEL_K8S_APP_NAME = "app.kubernetes.io/name"
LABEL_K8S_APP_TAG = "kubefox.xigxog.io/app-tag"
LABEL_K8S_APP_VERSION = "kubefox.xigxog.io/app-version"
LABEL_K8S_COMPONENT = "app.kubernetes.io/component"
LABEL_K8S_COMPONENT_HASH = "kubefox.xigxog.io/component-hash"
LABEL_K8S_COMPONENT_HASH_SHORT = "kubefox.xigxog.io/component-hash-short"
LABEL_K8S_COMPONENT_TYPE = "kubefox.xigxog.io/component-type"
LABEL_K8S_ENVIRONMENT = "kubefox.xigxog.io/environment"
LABEL_K8S_INSTANCE = "app.kubernetes.io/instance"
LABEL_K8S_PLATFORM = "kubefox.xigxog.io/platform"
LABEL_K8S_REL_MANIFEST = "kubefox.xigxog.io/release-manifest"
LABEL_K8S_RUNTIME_VERSION = "kubefox.xigxog.io/runtime-version"
LABEL_K8S_VIRTUAL_ENVIRONMENT = "kubefox.xigxog.io/virtual-environment"

# Kubernetes Annotations
ANNOTATION_LAST_APPLIED = "kubectl.kubernetes.io/last-applied-configuration"
ANNOTATION_TEMPLATE_DATA = "kubefox.xigxog.io/template-data"
ANNOTATION_TEMPLATE_DATA_HASH = "kubefox.xigxog.io/template-data-hash"

# Container Labels
LABEL_OCI_APP = "com.xigxog.kubefox.app"
LABEL_OCI_COMPONENT = "com.xigxog.kubefox.component"
LABEL_OCI_CREATED = "org.opencontainers.image.created"
LABEL_OCI_REVISION = "org.opencontainers.image.revision"
LABEL_OCI_SOURCE = "org.opencontainers.image.source"

FINALIZER_ENVIRONMENT_PROTECTION = "kubefox.xigxog.io/environment-protection"
FINALIZER_RELEASE_PROTECTION = "kubefox.xigxog.io/release-protection"

ENV_NODE_NAME = "KUBEFOX_NODE"
ENV_POD_IP = "KUBEFOX_POD_IP"
ENV_POD_NAME = "KUBEFOX_POD"

PLATFORM_COMPONENT_BOOTSTRAP = "bootstrap"
PLATFORM_COMPONENT_BROKER = "broker"
PLATFORM_COMPONENT_HTTPSRV = "httpsrv"
PLATFORM_COMPONENT_NATS = "nats"
PLATFORM_COMPONENT_OPERATOR = "operator"

CONDITION_TYPE_AVAILABLE = "Available"
CONDITION_TYPE_PROGRESSING = "Progressing"
CONDITION_TYPE_ACTIVE_RELEASE_AVAILABLE = "ActiveReleaseAvailable"
CONDITION_TYPE_RELEASE_PENDING = "ReleasePending"

CONDITION_REASON_BROKER_UNAVAILABLE = "BrokerUnavailable"
CONDITION_REASON_COMPONENT_DEPLOYMENT_FAILED = "ComponentDeploymentFailed"
CONDITION_REASON_COMPONENT_DEPLOYMENT_PROGRESSING = "ComponentDeploymentProgressing"
CONDITION_REASON_COMPONENTS_AVAILABLE = "ComponentsAvailable"
CONDITION_REASON_COMPONENTS_DEPLOYED = "ComponentsDeployed"
CONDITION_REASON_COMPONENT_UNAVAILABLE = "ComponentUnavailable"
CONDITION_REASON_CONTEXT_AVAILABLE = "ContextAvailable"
CONDITION_REASON_ENVIRONMENT_NOT_FOUND = "EnvironmentNotFound"
CONDITION_REASON_HTTPSRV_UNAVAILABLE = "HTTPSrvUnavailable"
CONDITION_REASON_NATS_UNAVAILABLE = "NATSUnavailable"
CONDITION_REASON_NO_RELEASE = "NoRelease"
CONDITION_REASON_PENDING_DEADLINE_EXCEEDED = "PendingDeadlineExceeded"
CONDITION_REASON_PLATFORM_COMPONENTS_AVAILABLE = "PlatformComponentsAvailable"
CONDITION_REASON_PROBLEMS_FOUND = "ProblemsFound"
CONDITION_REASON_RECONCILE_FAILED = "ReconcileFailed"
CONDITION_REASON_RELEASE_ACTIVATED = "ReleaseActivated"
CONDITION_REASON_RELEASE_PENDING = "ReleasePending"

# gRPC metadata keys.
GRPC_KEY_APP = "app"
GRPC_KEY_HASH = "hash"
GRPC_KEY_COMPONENT = "component"
GRPC_KEY_ID = "id"
GRPC_KEY_PLATFORM = "platform"
GRPC_KEY_POD = "pod"
GRPC_KEY_TOKEN = "token"
GRPC_KEY_TYPE = "type"

ARCHIVE_REASON_PENDING_DEADLINE_EXCEEDED = "PendingDeadlineExceeded"
ARCHIVE_REASON_ROLLED_BACK = "RolledBack"
ARCHIVE_REASON_SUPERSEDED = "Superseded"

PROBLEM_TYPE_ADAPTER_NOT_FOUND = "AdapterNotFound"
PROBLEM_TYPE_APP_DEPLOYMENT_FAILED = "AppDeploymentFailed"
PROBLEM_TYPE_APP_DEPLOYMENT_NOT_FOUND = "AppDeploymentNotFound"
PROBLEM_TYPE_DEPENDENCY_INVALID = "DependencyInvalid"
PROBLEM_TYPE_DEPENDENCY_NOT_FOUND = "DependencyNotFound"
PROBLEM_TYPE_DEPLOYMENT_FAILED = "DeploymentFailed"
PROBLEM_TYPE_DEPLOYMENT_NOT_FOUND = "DeploymentNotFound"
PROBLEM_TYPE_DEPLOYMENT_UNAVAILABLE = "DeploymentUnavailable"
PROBLEM_TYPE_PARSE_ERROR = "ParseError"
PROBLEM_TYPE_POLICY_VIOLATION = "PolicyViolation"
PROBLEM_TYPE_REL_MANIFEST_FAILED = "ReleaseManifestFailed"
PROBLEM_TYPE_REL_MANIFEST_NOT_FOUND = "ReleaseManifestNotFound"
PROBLEM_TYPE_REL_MANIFEST_UNAVAILABLE = "ReleaseManifestUnavailable"
PROBLEM_TYPE_ROUTE_CONFLICT = "RouteConflict"
PROBLEM_TYPE_VAR_NOT_FOUND = "VarNotFound"
PROBLEM_TYPE_VAR_WRONG_TYPE = "VarWrongType"
PROBLEM_TYPE_VERSION_CONFLICT = "VersionConflict"

DATA_SOURCE_KIND_VIRTUAL_ENVIRONMENT = "VirtualEnvironment"

PROBLEM_SOURCE_KIND_APP_DEPLOYMENT = "AppDeployment"
PROBLEM_SOURCE_KIND_COMPONENT = "Component"
PROBLEM_SOURCE_KIND_DEPLOYMENT = "Deployment"
PROBLEM_SOURCE_KIND_HTTP_ADAPTER = "HTTPAdapter"
PROBLEM_SOURCE_KIND_REL_MANIFEST = "ReleaseManifest"
PROBLEM_SOURCE_KIND_VIRTUAL_ENV = "VirtualEnvironment"

ENV_VAR_TYPE_ARRAY = "Array"
ENV_VAR_TYPE_BOOLEAN = "Boolean"
ENV_VAR_TYPE_NUMBER = "Number"
ENV_VAR_TYPE_STRING = "String"

COMPONENT_TYPE_BROKER = "Broker"
# COMPONENT_TYPE_DATABASE_ADAPTER = "DBAdapter"
COMPONENT_TYPE_HTTP_ADAPTER = "HTTPAdapter"
COMPONENT_TYPE_KUBEFOX = "KubeFox"
COMPONENT_TYPE_NATS = "NATS"


def is_adapter(c):
    if c == COMPONENT_TYPE_HTTP_ADAPTER:
        return True
    else:
        return False


RELEASE_TYPE_STABLE = "Stable"
RELEASE_TYPE_TESTING = "Testing"

FOLLOW_REDIRECTS_ALWAYS = "Always"
FOLLOW_REDIRECTS_NEVER = "Never"
FOLLOW_REDIRECTS_SAME_HOST = "SameHost"

EVENT_TYPE_CRON = "io.kubefox.cron"
EVENT_TYPE_DAPR = "io.kubefox.dapr"
EVENT_TYPE_HTTP = "io.kubefox.http"
EVENT_TYPE_KUBEFOX = "io.kubefox.kubefox"
EVENT_TYPE_KUBERNETES = "io.kubefox.kubernetes"

EVENT_TYPE_ACK = "io.kubefox.ack"
EVENT_TYPE_BOOTSTRAP = "io.kubefox.bootstrap"
EVENT_TYPE_ERROR = "io.kubefox.error"
EVENT_TYPE_HEALTH = "io.kubefox.health"
EVENT_TYPE_METRICS = "io.kubefox.metrics"
EVENT_TYPE_NACK = "io.kubefox.nack"
EVENT_TYPE_REGISTER = "io.kubefox.register"
EVENT_TYPE_REJECTED = "io.kubefox.rejected"
EVENT_TYPE_TELEMETRY = "io.kubefox.telemetry"
EVENT_TYPE_UNKNOWN = "io.kubefox.unknown"

# Keys for well known values.
VAL_KEY_HEADER = "header"
VAL_KEY_HOST = "host"
VAL_KEY_MAX_EVENT_SIZE = "maxEventSize"
VAL_KEY_METHOD = "method"
VAL_KEY_PATH = "path"
VAL_KEY_PATH_SUFFIX = "pathSuffix"
VAL_KEY_QUERY = "queryParam"
VAL_KEY_STATUS = "status"
VAL_KEY_STATUS_CODE = "statusCode"
VAL_KEY_URL = "url"
VAL_KEY_VAULT_URL = "vaultURL"
VAL_KEY_SPEC = "spec"

# Headers and query params.
HEADER_ADAPTER = "kubefox-adapter"
HEADER_APP_DEPLOYMENT = "kubefox-app-deployment"
HEADER_APP_DEPLOYMENT_ABBRV = "kf-dep"
HEADER_CONTENT_LENGTH = "Content-Length"
HEADER_CONTENT_TYPE = "Content-Type"
HEADER_EVENT_ID = "kubefox-event-id"
HEADER_EVENT_TYPE = "kubefox-event-type"
HEADER_EVENT_TYPE_ABBRV = "kf-type"
HEADER_HOST = "Host"
HEADER_PLATFORM = "kubefox-platform"
HEADER_REL_MANIFEST = "kubefox-release-manifest"
HEADER_TELEMETRY_SAMPLE = "kubefox-telemetry-sample"
HEADER_TELEMETRY_SAMPLE_ABBRV = "kf-sample"
HEADER_TRACE_ID = "kubefox-trace-id"
HEADER_VIRTUAL_ENV = "kubefox-virtual-environment"
HEADER_VIRTUAL_ENV_ABBRV = "kf-ve"

CHARSET_UTF8 = "charset=UTF-8"

DATA_SCHEMA_EVENT = "kubefox.proto.v1.Event"

CONTENT_TYPE_HTML = "text/html"
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_PLAIN = "text/plain"
CONTENT_TYPE_PROTOBUF = "application/protobuf"

REGEXP_COMMIT = re.compile(r"^[0-9a-f]{40}$")
REGEXP_GIT_REF = re.compile(r"^[a-z0-9][a-z0-9-\\.]{0,28}[a-z0-9]$")
REGEXP_HASH = re.compile(r"^[0-9a-f]{32}$")
REGEXP_IMAGE = re.compile(r"^.*:[a-z0-9-]{40}$")
REGEXP_NAME = re.compile(r"^[a-z0-9][a-z0-9-]{0,28}[a-z0-9]$")
REGEXP_UUID = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

KUBEFOX_HOME = os.getenv("KUBEFOX_HOME", os.path.join("/", "tmp", "kubefox"))

FILE_CA_CERT = "ca.crt"
FILE_TLS_CERT = "tls.crt"
FILE_TLS_KEY = "tls.key"

PATH_CA_CERT = os.path.join(KUBEFOX_HOME, FILE_CA_CERT)
PATH_SVC_ACC_TOKEN = "/var/run/secrets/kubernetes.io/serviceaccount/token"
PATH_TLS_CERT = os.path.join(KUBEFOX_HOME, FILE_TLS_CERT)
PATH_TLS_KEY = os.path.join(KUBEFOX_HOME, FILE_TLS_KEY)

DEFAULT_ROUTE_ID = -1
