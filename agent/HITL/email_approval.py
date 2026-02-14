import json


def email_human_approval(email: dict):
    """
    Human-in-the-loop approval for email sending.
    """

    # email = json.loads(email_draft_json)

    print("\n----- EMAIL DRAFT -----")
    print(f"Subject: {email['subject']}\n")
    print(email["body"])
    print("-----------------------")

    print("\nChoose an action:")
    print("1. Send")
    print("2. Edit")
    print("3. Cancel")

    choice = input("Enter choice (1/2/3): ").strip()

    if choice == "1":
        return "SEND", None

    elif choice == "2":
        instruction = input(
            "\nWhat would you like to change? (e.g. make it formal, shorten, add apology)\n"
        )
        return "EDIT", instruction

    else:
        return "CANCEL", None
