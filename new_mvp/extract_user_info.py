from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text
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
                id="school",
                description = "The university a college students attend.",
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
                {"school": "University of California, Irvine"},
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
                "I'm a PhD student currently in Stanford University. I've studied 4 years in University of California, Irvine, majoring \
                    in computer science. Now i wish to pursue computer engineering. Can you give me some resources on computer science?",
                    [
                        {"intended_major": "computer science", "school": ["Stanford University", "University of California, Irvine"]},
                    ]
            ),
            (
                "I'm ready to be a graduate student in University of California, Los Angeles. Before that I'm a graduate student in Harvard \
                University. Can you give me some resources in UCLA?",
                [{"school": ["Harvard University", "University of California, Los Angeles"]}]
            )

        ]

    )

def extract_User_info(llm, question):
    chain_user_info = create_extraction_chain(llm,person_schema)
    return chain_user_info(question)