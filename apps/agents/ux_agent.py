import re

def load_prompt(file_name):
    with open(f"data/prompts/{file_name}", "r") as f:
        return f.read()

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
    if "persona" in text:
        return ["persona"]
    if "journey" in text:
        return ["journey"]
    if "design brief" in text or "onboarding" in text:
        return ["design"]
    return ["design"]


# =========================================================
# DOMAIN (INPUT-RESPECTING)
# =========================================================
def generate_what(context, user_input):
    return (
        "A platform based on the given context, focused on addressing key user experience challenges"
        "and improving the overall flow."
    )
    
# =========================================================
# GOAL (UX-SPECIFIC)
# =========================================================
def generate_goal(context):
    exp = context["experience"]

    if exp == "onboarding":
        return (
            "To improve onboarding completion by reducing friction in identity verification, "
            "improving system feedback during errors, and enabling users to recover from failures, "
            "resulting in smoother progression from entry to successful account activation."
        )

    if exp == "checkout":
        return (
            "To improve successful transaction completion by reducing failures during payment processing, "
            "improving clarity of payment options, and enabling recovery from transaction errors, "
            "resulting in fewer abandoned transactions."
        )

    return (
        "To improve task completion by reducing interaction friction and improving system feedback, "
        "resulting in smoother user progression through key flows."
    )

#==========================================================
# BUILD (NEW - CONTEXT AWARE)
#==========================================================
def generate_build(context):
    exp = context["experience"]
    if exp == "onboarding":
        return (
            "A seamless onboarding experience that simplifies flows, improves system feedback,"
            "and enables users to recover from errors, resulting in smoother account activation."
            )
    if exp == "checkout":
        return (
            "A seamless checkout experience that reduces friction during payment, improve clarity"
            "of steps, and enables recovery from transaction failures, resulting in higher completion rates."
            )
    retutn (
        "An improved user experience that reduces friction, improves clarity and enables smoother task completion."
    )
    
# =========================================================
# USER PROBLEMS
# =========================================================
def generate_user_problems(context):
    if context["experience"] == "onboarding":
        return [
            {
                "problem": "It is difficult to complete onboarding because OTP failures and unclear retry handling during verification which affects successful account activation.",
                "outcome": "By improving OTP handling and retry flows, users are able to complete verification successfully, increasing account activation rates."
            },
            {
                "problem": "There is friction during document upload because file requirements and validation errors are not clearly communicated which affects completion rates.",
                "outcome": "By providing clear upload guidelines and real-time validation feedback, users are able to complete document submission without errors."
            },
            {
                "problem": "It is frustrating to continue onboarding because session timeouts and lack of progress saving which affects task continuity and increases abandonment.",
                "outcome": "By enabling session persistence and progress saving, users are able to resume onboarding without restarting, reducing drop-offs."
            }
        ]

    return [
        {
            "problem": "Users face friction due to unclear interaction flows which affects task completion.",
            "outcome": "By improving interaction clarity, users can complete tasks more efficiently."
        }
    ]


# =========================================================
# BUSINESS PROBLEMS
# =========================================================
def generate_business_problems(context):
    if context["experience"] == "onboarding":
        return [
            {
                "problem": "There is loss of potential users because onboarding friction leads to drop-offs which affects acquisition.",
                "outcome": "By reducing onboarding friction, more users complete the process, improving acquisition."
            },
            {
                "problem": "There is increased operational effort because failed onboarding requires manual intervention which affects efficiency.",
                "outcome": "By improving flow success rates, operational overhead is reduced."
            }
        ]

    return [
        {
            "problem": "Business performance is impacted due to user friction in key flows.",
            "outcome": "By improving flows, business outcomes improve."
        }
    ]


# =========================================================
# SCOPE
# =========================================================
def generate_scope(context):
    if context["experience"] == "onboarding":
        return """Customer – (New users onboarding) – Mobile (iOS/Android 360px-414px)

• Onboarding Experience
o Initiating onboarding and understanding requirements
o Entering personal details with validation feedback
o Uploading documents and handling validation errors
o Completing OTP verification with retry and fallback options
o Recovering from errors (timeouts, failed verification)
o Resuming incomplete onboarding flows
o Completing onboarding and accessing account

Customer Support – (Handling onboarding issues) – Desktop (1366px-1920px)

• Support Experience
o Viewing onboarding status and failure points
o Assisting users with verification and document issues
o Resolving incomplete onboarding cases
"""
    return """Customer – (General experience) – Mobile"""


# =========================================================
# ARTIFACT MAPPER (DYNAMIC)
# =========================================================
def map_artifacts(context, user_problems, business_problems):
    artifacts = set()

    all_text = " ".join(
        [p["problem"].lower() for p in user_problems + business_problems]
    )

    if any(word in all_text for word in ["drop-off", "flow", "navigation", "abandon"]):
        artifacts.update(["Journey Maps", "User Flows"])

    if any(word in all_text for word in ["otp", "error", "validation", "upload", "failure"]):
        artifacts.update(["Experience Audit", "Wireframes"])

    if any(word in all_text for word in ["multiple", "steps", "dependency", "process"]):
        artifacts.update(["Ecosystem Map", "User Flows"])

    if any(word in all_text for word in ["understand", "confusion", "unclear"]):
        artifacts.update(["Personas", "Journey Maps"])

    if context["experience"] == "onboarding":
        artifacts.add("Experience Audit")

    if not artifacts:
        artifacts.update([
            "Personas",
            "Journey Maps",
            "Ecosystem Map",
            "Experience Audit",
            "User Flows",
            "Wireframes"
        ])

    return sorted(list(artifacts))


# =========================================================
# RENDER ARTIFACTS
# =========================================================
def render_artifacts(artifacts):
    return "\n".join([f"• {a}" for a in artifacts])


# =========================================================
# FORMAT CONTRACT
# =========================================================
def render_design_brief(sections):
    return f"""Design Brief

1. Background

1.1 What is it?
{sections['what']}

1.2 What are you trying to build?
{sections['build']}

1.3 Who are all the users involved and what is their primary responsibility?

Primary Users:
• {sections['primary_user']}

Secondary Users:
• {sections['secondary_users']}

2. Goal

{sections['goal']}

3. Problems & Outcomes

USERS

| User Type | Problems | Outcomes |
|----------|----------|----------|
{sections['user_rows']}

BUSINESS

| Business User | Problems | Outcomes |
|--------------|----------|----------|
{sections['business_rows']}

4. Scope

{sections['scope']}

5. Stakeholders

Driver: [Driver Full Name]
Approver: [Approver Full Name]
Contributors: [Member 1 Full Name, Member 2 Full Name]
SMEs: [SME 1 Full Name, SME 2 Full Name]
Informed: [Member 1 Full Name, Member 2 Full Name]

6. Timelines

Overall Duration: [Date-Month-Year - Date-Month-Year]

Date Key Milestone
Date-Month-Year - Date-Month-Year Milestone 1
Date-Month-Year Milestone 2

7. Artifacts

{sections['artifacts']}
"""


# =========================================================
# DESIGN AGENT
# =========================================================
def design_agent(user_input):
    prompt_template = load_prompt("design_brief.txt")
    full_prompt = f"{prompt_template}\n\nUser Input:\n{user_input}"
    context = parse_context(user_input)

    user_problems = generate_user_problems(context)
    business_problems = generate_business_problems(context)

    user_rows = ""
    for p in user_problems:
        user_rows += f"| Customer | {p['problem']} | {p['outcome']} |\n"

    business_rows = ""
    for p in business_problems:
        business_rows += f"| Platform | {p['problem']} | {p['outcome']} |\n"

    artifacts = map_artifacts(context, user_problems, business_problems)

    sections = {
        "what": generate_what(context, user_input),
        "build": generate_build(context),
        "primary_user": "Customer – Completes onboarding and uses the platform",
        "secondary_users": "Customer Support – Assists users\n• Operations – Monitors flows\n• Compliance – Ensures requirements",
        "goal": generate_goal(context),
        "user_rows": user_rows,
        "business_rows": business_rows,
        "scope": generate_scope(context),
        "artifacts": render_artifacts(artifacts)
    }

    return render_design_brief(sections)


# =========================================================
# CRITIC AGENT
# =========================================================
def critic_agent(output):
    feedback = []

    if "OTP" not in output:
        feedback.append("Missing verification flow depth")
        
    if "error" not in output:
        feedback.append("Missing error handling clarity")
    if feedback:
        output += "\n\n(Refined to include better handling f verification and error scenarios.)"
    return output


# =========================================================
# ORCHESTRATOR
# =========================================================
def run_agent(user_input):
    design_output = design_agent(user_input)
    final_output = critic_agent(design_output)

    print("\n")
    print("Here’s your thoughtful UX response:\n")
    print(final_output)

    return final_output


# =========================================================
# ENTRY
# =========================================================
if __name__ == "__main__":
    run_agent("Design checkout experience for Amazon where users drop off due to payment failures and lack of trust signals during order placement")
