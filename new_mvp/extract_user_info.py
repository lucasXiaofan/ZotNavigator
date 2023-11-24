from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text
# Extract User info
person_schema = Object(
        id="person",
        description="Personal information about a college student",
        attributes = [
            Text(
                id="current_major",
                description = "The current major of a college student.",
            ),
            Text(
                id="intended_major",
                description = "A student's academic interest.",
            ),
            Text(
                id="tags",
                description = "student's personal interest, favorite",
            ),
            Text(
                id="goals",
                description = "student's personal, academic, goals",
            ),
            Text(
                id = "year",
                description="The year a college student is currently at",
            )
        
        ],
        examples = [
            ("Hello. My name is Alexander, a freshman from University of California, Irvine. My major is currently computer science \
            and I want to do some projects in computer science",
            [
                {"current_major": "computer science"},
                {"intended_major": "computer science"},
                {"year": "freshman"}
            ]
            ),
            (
                "My major is currently computer engineering, but I wish to transfer to computer science. \
                Do you know how to transfer to computer science?",
                [
                    {"current_major": "computer engineering"},
                    {"intended_major": "computer science"},
                ]
            ),
            (
                "I am looking for ML research opportunities do you have any suggestions?",
                [
                    {'goals':'Machine learning research'},
                    {'tags':['ML','Research']},
                ]
            ),
            (
                "where can I find on campus music conference?",
                [
                    {'tags':['Music']},
                ]
            ),
            (
                "how can I report my professor?",
                [
                    {'tags':"None"},
                ]
            ),

        ]

    )
def extract_User_info(llm, question):
    chain_user_info = create_extraction_chain(llm,person_schema)
    return chain_user_info(question)