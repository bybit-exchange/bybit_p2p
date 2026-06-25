import warnings

from .p2p_requests import P2PRequests

_DEPRECATION_WARNING_MESSAGE = (
    "bybit_p2p is deprecated and will receive no new features. "
    "Please migrate to pybit: https://pypi.org/project/pybit/"
)
_deprecation_warning_emitted = False


class P2P(
    P2PRequests
):
    def __init__(self, **args):
        global _deprecation_warning_emitted

        if not _deprecation_warning_emitted:
            warnings.warn(
                _DEPRECATION_WARNING_MESSAGE,
                FutureWarning,
                stacklevel=2,
            )
            _deprecation_warning_emitted = True

        super().__init__(**args)
