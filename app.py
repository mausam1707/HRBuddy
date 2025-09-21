from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from teams_bot import TeamsBot
from config import TEAMS_APP_ID, TEAMS_APP_PASSWORD, BOT_PORT

settings = BotFrameworkAdapterSettings(TEAMS_APP_ID, TEAMS_APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)
bot = TeamsBot()

async def handle_messages(req):
    try:
        body = await req.json()
        activity = Activity.deserialize(body)
        auth_header = req.headers.get('Authorization', '')
        await adapter.process_activity(activity, auth_header, bot.on_turn)
        return web.Response(status=200)
    except Exception as e:
        print(f"Error handling request: {e}")
        return web.Response(status=500)

def main():
    app = web.Application()
    app.router.add_post('/api/messages', handle_messages)

    print(f"Bot running on http://localhost:{BOT_PORT}")
    try:
        web.run_app(app, port=BOT_PORT)
    except KeyboardInterrupt:
        print("Bot stopped.")

if __name__ == '__main__':
    main()
