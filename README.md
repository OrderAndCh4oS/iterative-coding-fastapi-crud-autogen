# Iterative Coding FastAPI CRUD with Autogen

Welcome to Iterative Coding FastAPI CRUD with Autogen! This project leverages the capabilities of Autogen and OpenAI to generate, review, and refine a RESTful API for managing customer data using FastAPI.

## Table of Contents

- [Overview](#overview)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Features](#features)
- [Contribution](#contribution)
- [License](#license)

## Overview

This framework is designed to automate the process of developing a CRUD FastAPI service. It follows an iterative approach, where:

1. The AI assistant develops code according to a given spec.
2. A quality assurance (QA) agent reviews the generated code and provides feedback.
3. The AI assistant then refines its work based on the QA feedback, resulting in a polished end product.

## Installation & Setup

1. Clone the repository:

```bash
git clone https://github.com/your-github-username/iterative-coding-fastapi-crud-autogen.git
cd iterative-coding-fastapi-crud-autogen
```

## Usage

1. Configure the desired API spec and assistant rules in the `main.py` file.
2. Run the script:

```bash
python main.py
```

3. Review the generated code, QA feedback, and any TODOs in the specified output directory.

## Features

- **Autogen Integration:** Leverages Autogen to manage agent-based interactions and code generation.
- **Iterative Development:** The assistant and QA agents work together to iteratively refine the code.
- **Flexible Configuration:** Easily specify your desired API requirements and let the assistant handle the implementation.
  
## Contribution

Contributions are welcome! Please raise an issue or submit a pull request.
