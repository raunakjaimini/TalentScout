def tech_question_prompt(tech_stack):
    return (
        f"Generate 3 technical questions for a candidate proficient in the following technologies: {tech_stack},"
        "Ensure the questions assess their proficinecy in the technologies listed."
    )