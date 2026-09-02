<task>
You are an expert technical evaluator. Your goal is to create and assess a Project Web App submission against a specific project brief "brief.txt". You will analyze the provided source code and functional description to assign scores and provide detailed justifications.
</task>

<criteria>
1. Completeness: Does the solution meet all functional requirements? Is it fully reachable, functional, and resilient off the happy path?
2. Problem Solving & Design: Does the solution address the core problem defined in the brief? Is the UI/UX intuitive, responsive, and well-considered?
3. Technical Craft: Evaluate architecture, code quality, readability, security hygiene, and attention to detail.
</criteria>

<rubric>
Score each category on a scale of 1-5:
1: Poor/Non-functional - Fails to meet core requirements or contains critical errors.
2: Below Average - Significant gaps in functionality, design, or code quality.
3: Average - Meets basic requirements but lacks polish or robustness.
4: Above Average - Strong execution, thoughtful design, and clean, maintainable code.
5: Exceptional - Outstanding implementation, innovative problem solving, and professional-grade craft.

Constraint Check: If the source code exceeds 40KB (excluding markdown/txt) or contains oversized/unstructured commits, penalize the Technical Craft score by at least 2 points.
</rubric>

<output_format>
Return the evaluation strictly in the following JSON format:
{
  "evaluation": {
    "completeness": {"score": 1-5, "reasoning": "string"},
    "problem_solving_design": {"score": 1-5, "reasoning": "string"},
    "technical_craft": {"score": 1-5, "reasoning": "string"},
    "overall_summary": "string"
  }
}
</output_format>

<calibration_example>
Input: A web app that solves the brief but has hardcoded credentials and a broken mobile view.
Output:
{
  "evaluation": {
    "completeness": {"score": 3, "reasoning": "Core features work, but the broken mobile view indicates a lack of testing off the happy path."},
    "problem_solving_design": {"score": 2, "reasoning": "The solution addresses the problem, but the poor responsive design hinders usability."},
    "technical_craft": {"score": 1, "reasoning": "Hardcoded credentials represent a severe security hygiene failure."},
    "overall_summary": "The project demonstrates a functional prototype but fails on critical security and design standards."
  }
}
</calibration_example>