from kiteconnect import KiteConnect

from app.config import settings


def main() -> None:
    if not settings.kite_api_key:
        raise ValueError("Missing KITE_API_KEY in environment.")
    if not settings.kite_api_secret:
        raise ValueError("Missing KITE_API_SECRET in environment.")

    kite = KiteConnect(api_key=settings.kite_api_key)
    login_url = kite.login_url()

    print("Open this URL in your browser and complete Kite login:")
    print(login_url)
    print()
    request_token = input("Paste request_token from redirect URL: ").strip()

    if not request_token:
        raise ValueError("request_token is required.")

    session = kite.generate_session(request_token, api_secret=settings.kite_api_secret)
    access_token = session.get("access_token")
    user_name = session.get("user_name")

    print()
    print("KITE ACCESS TOKEN:")
    print(access_token)
    if user_name:
        print()
        print("KITE USER NAME:")
        print(user_name)

    try:
        kite.set_access_token(access_token)
        profile = kite.profile()
        print()
        print("VERIFIED ACCESS TOKEN")
        print("user_name:", profile.get("user_name", "N/A"))
    except Exception as exc:
        print()
        print("TOKEN VERIFICATION FAILED:")
        print(str(exc))


if __name__ == "__main__":
    main()
