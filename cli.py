import argparse

from support import SupportService

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLI tools for the MA Politics analysis suite')
    parser.add_argument('--suite', help="Which CLI suite to run", required=True)
    parser.add_argument('--method', help="Which CLI method to run", required=True)
    parser.add_argument('--supplement', help="Any supporting data", required=False)

    args = parser.parse_args()

    if args.suite == "support":
        support_service = SupportService()

        if args.method == "get-language":
            print(support_service.compose_language())

        elif args.method == "create-senate-stats":
            support_service.create_senate_stats()

        elif args.method == "create-house-stats":
            support_service.create_house_stats()

        elif args.method == "get-averages":
            support_service.get_avgs()