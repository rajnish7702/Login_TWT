from werkzeug.middleware.dispatcher import (
    DispatcherMiddleware,
)  
from accounts import user_accounts
camcom = user_accounts()

application = DispatcherMiddleware(
    camcom,
    {        
    },
)
