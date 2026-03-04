from client_auth import ClientAuth, pick_method


def main():
    method = pick_method()
    user = ClientAuth(method)
    print('hi')


if __name__ == '__main__':
    main()
