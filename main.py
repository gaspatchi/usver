from aiohttp import web
from middlewares.auth import verifyAuth
from middlewares.validate import validateJson
from routes.metrics import showMetrics
from routes.users import (loginUser, registerUser, resetPassword,
                          selectProfile, updateProfile, verifyToken)
from utils.config import config
from utils.hooks import registerService, shutdowService

app = web.Application(middlewares=[validateJson,verifyAuth])

app.router.add_get("/", selectProfile)
app.router.add_patch("/", updateProfile)
app.router.add_post("/login", loginUser)
app.router.add_post("/register", registerUser)
app.router.add_get("/verification/{token}",verifyToken)
app.router.add_post("/reset", resetPassword)
app.router.add_get("/metrics", showMetrics)

app.on_startup.append(registerService)
app.on_shutdown.append(shutdowService)

web.run_app(app,host=config["server"]["address"],port=config["server"]["port"])
