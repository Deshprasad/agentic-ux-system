import re


# =========================================================

# CORE ENGINE

# =========================================================

def core_engine(user_input):

    context = parse_context(user_input)

    return {

        "context": context,

        "user_input": user_input,

        "experience": context.get("experience", "general"),

        "goal": generate_goal(context),

        "user_problems": generate_user_problems(context),

        "business_problems": generate_business_problems(context)

    }


# =========================================================

# CONTEXT PARSER

# =========================================================

def parse_context(user_input):

    text = user_input.lower()

    if "onboarding" in text:

        experience = "onboarding"

    elif "checkout" in text:

        experience = "checkout"

    else:

        experience = "general"

    return {"experience": experience}


# =========================================================

# STRATEGIST

# =========================================================

def strategist(user_input):

    text = user_input.lower()

    if any(w in text for w in ["design", "experience", "flow", "brief"]):
        return "design"

    if any(w in text for w in ["persona", "user type", "target user"]):
        return "persona"

    if any(w in text for w in ["journey", "experience map"]):
        return "journey"

    return "design"


# =========================================================

# GOAL

# =========================================================

def generate_goal(context):

    exp = context["experience"]

    if exp == "onboarding":

        return (

            "To improve onboarding completion by reducing friction in verification and enabling recovery from failures, "

            "resulting in smoother user progression and reduced drop-offs."

        )

    if exp == "checkout":

        return (

            "To improve transaction success by reducing payment failures and improving clarity, "

            "resulting in higher completion rates."

        )

    return (

        "To improve task completion by reducing friction and improving clarity, "

        "resulting in smoother user progression."

    )


# =========================================================

# BUILD

# =========================================================

def generate_build(context):

    exp = context["experience"]

    if exp == "onboarding":

        return (

            "Design a seamless onboarding experience that reduces user effort, improves clarity, "

            "and enables recovery from failures."

        )

    if exp == "checkout":

        return (

            "Design a seamless checkout experience that reduces payment failures and improves clarity."

        )

    return "Design an improved experience that reduces friction."


# =========================================================

# BACKGROUND 

# =========================================================

def generate_background(context):

    exp = context["experience"]

    return f"""The organization operates a digital platform supporting {exp} experiences.

Core business:

• Enables users to complete key workflows digitally

Primary challenges:

• Friction in critical steps

• Drop-offs due to failures and unclear recovery

Existing landscape:

• Key components: Application UI, backend services, validation systems

• External dependencies: APIs, third-party services (e.g., OTP/payment systems)

• Data flow: User input → validation → processing → system response

• Control/decision points: Validation checks, retries, error handling

• Storage/state mechanism: Session handling and backend persistence

"""


# =========================================================

# USER PROBLEMS 

# =========================================================

def generate_user_problems(context):

    if context["experience"] == "onboarding":

        return [

            {

                "problem": "It is frustrating because OTP failures occur frequently which affects completing onboarding successfully.",

                "outcomes": [

                    "By improving OTP handling, users complete verification successfully.",

                    "By reducing retries, users experience smoother onboarding."

                ]

            },

            {

                "problem": "It is confusing because retry options are unclear which affects user confidence.",

                "outcomes": [

                    "By improving retry clarity, users proceed without confusion."

                ]

            }

        ]

    return [

        {

            "problem": "It is difficult because flows are unclear which affects task completion.",

            "outcomes": [

                "By improving clarity, users complete tasks efficiently."

            ]

        }

    ]


# =========================================================

# BUSINESS PROBLEMS

# =========================================================

def generate_business_problems(context):

    return [

        {

            "problem": "There is loss of potential users because onboarding friction leads to drop-offs which affects acquisition.",

            "outcomes": [

                "By reducing friction, more users complete onboarding.",

                "By improving completion, acquisition improves."

            ]

        }

    ]


# =========================================================

# TABLE BUILDER 

# =========================================================

def build_table(rows, user_type, header):

    table = f"| {header} | Problems | Outcomes |\n"

    table += "|----------|----------|----------|\n"

    for r in rows:

        outcomes = "<br><br>".join(r["outcomes"])

        table += f"| {user_type} | {r['problem']} | {outcomes} |\n"

    return table


# =========================================================

# SCOPE

# =========================================================

def generate_scope(context):

    exp = context["experience"]

    return f"""Customer ({exp} experience) – Mobile

Primary workflows:

• Completing key steps

• Validation and submission

Secondary workflows:

• Retry handling

• Error recovery

Supporting activities:

• System feedback

• Support interaction

"""


# =========================================================

# DESIGN AGENT

# =========================================================

def design_agent(user_input):

    data = core_engine(user_input)

    context = data["context"]

    user_table = build_table(data["user_problems"], "Customer", "User Type")

    business_table = build_table(data["business_problems"], "Platform", "Business User")

    return f"""Design Brief

1. Background

1.1 What is it?

{generate_background(context)}

1.2 What are you trying to build?

{generate_build(context)}

1.3 Who are all the users involved and what is their primary responsibility?

Primary Users:

• Customer – Completes tasks within the experience

Secondary Users:

• Support – Assists users

• Operations – Monitors flows

2. Goal

{data['goal']}

3. Problems & Outcomes

USERS

{user_table}

BUSINESS

{business_table}

4. Scope

{generate_scope(context)}

5. Stakeholders

Driver: [Driver Full Name]
Approver: [Approver Full Name]
Contributors: [Member 1 Full Name, Member 2 Full Name]
SMEs: [SME 1 Full Name, SME 2 Full Name]
Informed: [Member 1 Full Name, Member 2 Full Name]

6. Timelines

6. Timelines

Overall Duration: [Date-Month-Year - Date-Month-Year]

Date Key Milestone
Date-Month-Year - Date-Month-Year Milestone 1
Date-Month-Year Milestone 2

7. Artifacts

• Personas
• Journey Maps
• Ecosystem Map
• Experience Audit
• User Flows
• Wireframes

"""


# =========================================================

# PERSONA AGENT

# =========================================================

def persona_agent(user_input):

    data = core_engine(user_input)

    pain_points = ""

    for p in data["user_problems"]:

        pain_points += f"- {p['problem']}\n"

    return f"""A user navigating a {data['context']['experience']} experience.

Goal:

{data['goal']}

Challenges:

{pain_points}

"""


# =========================================================

# JOURNEY AGENT

# =========================================================

def journey_agent(user_input):

    return "Journey Mapping Agent is under development."


# =========================================================

# ORCHESTRATOR

# =========================================================

def run_agent(user_input):

    task = strategist(user_input)

    if task == "persona":

        result = persona_agent(user_input)

    elif task == "journey":

        result = journey_agent(user_input)

    else:

        result = design_agent(user_input)

    print("\n")

    print(result)

    return result


# =========================================================

# ENTRY

# =========================================================

if __name__ == "__main__":

    run_agent("Design onboarding experience for users facing OTP failures and document upload errors")
 