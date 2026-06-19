from src.query import query_rag


def start_chatbot():

    print("\n" + "=" * 50)
    print("Document Q&A Bot")
    print("=" * 50)

    print("\nAsk questions about your documents.")
    print("Type 'exit' to quit.\n")

    while True:

        user_question = input("Question: ")

        if user_question.lower() == "exit":
            print("\nGoodbye!")
            break

        try:

            result = query_rag(
                user_question
            )

            print("\nAnswer:\n")
            print(result["answer"])

            print("\n" + "-" * 50)

        except Exception as error:

            print(
                f"\nError: {error}"
            )


if __name__ == "__main__":
    start_chatbot()