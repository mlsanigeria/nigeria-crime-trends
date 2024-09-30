# Contributing to the Hacktoberfest Repository

Welcome to the **Nigeria Crime Trends** project repository, organized by the Microsoft Learn Student Ambassadors for Hacktoberfest 2024! This repository focuses on **Crime Trend Analysis and Fatality Prediction in Nigeria (1997 - 2024)**. We're thrilled to have you contribute to this important project aimed at analyzing crime patterns and predicting fatalities based on available historical data.

## How to Install Dependencies and Work on the Project Locally

1. **Clone the Repository:**

   From your terminal, clone your forked repository and name it `nigeria-crime-trends`.

   ```bash
   # Replace {user_name} with your GitHub username
   git clone https://github.com/{user_name}/nigeria-crime-trends.git
   ```

2. **Set Up Virtual Environment:**

   Create a virtual environment named `nigeria-crime-trends`.

   ```bash
   # Windows
   python -m venv nigeria-crime-trends

   # macOS or Linux
   python3 -m venv nigeria-crime-trends
   ```

   Activate the virtual environment:

   ```bash
   # Windows
   nigeria-crime-trends\Scripts\activate

   # macOS or Linux
   source nigeria-crime-trends/bin/activate
   ```

   Install necessary dependencies:

   ```bash
   cd nigeria-crime-trends
   pip install -r requirements.txt
   ```

   Add the virtual environment to Jupyter Kernel if necessary:

   ```bash
   python -m ipykernel install --user --name=nigeria-crime-trends
   ```

3. **Work on the Project:**

   - This repository is dedicated to analyzing and predicting crime trends and fatalities in Nigeria. Review the **Issues** tab for tasks or suggestions you can tackle.
   - Go through the existing codebase, especially focusing on data cleaning, analysis, and modeling, and contribute to improving the prediction algorithms.
   - You can check out [this notebook](https://github.com/Sammybams/HamoyeAI-Team-Theano-Capstone-Project/blob/master/experimentation/Full%20Analysis%20of%20Crime%20Dataset%20(1997%20to%202023%20March%2031st).ipynb), which contains a full analysis of crime trends across Africa. It provides a comprehensive approach that can guide or inspire your work as you analyze and predict crime trends and fatalities specifically for Nigeria.

4. **Commit and Push Your Changes:**

   Once your contributions are ready, commit your changes and push them to your forked repository.

   ```bash
   git add .
   git commit -m "{COMMIT_MESSAGE}"
   git push
   ```

5. **Submit a Pull Request:**

   After pushing your changes, submit a pull request to merge them into the main repository. Be sure to include a clear and concise description of what your contribution entails.

## How You Can Contribute:

1. Review the project and current issues related to crime trend analysis and prediction.
2. Select an open issue, whether it's related to data cleaning, model improvements, or any other aspect of the project.
3. Test your contribution thoroughly and ensure that it aligns with the overall project goals.
4. Submit your pull request with a detailed explanation of your contribution.

## ✔️ General Contribution Guidelines

- Follow coding best practices, including writing clean, modular, and well-documented code.
- Provide meaningful commit messages and clear pull request descriptions.
- Collaborate respectfully and actively engage with other contributors.
- Don’t hesitate to reach out to project maintainers if you have any questions or need assistance.

**Happy hacking! We look forward to your amazing contributions!**

---

## 🔗 Links to Resources

1. [How to Do Your First Pull Request](https://youtu.be/nkuYH40cjo4?si=Cb6U2EKVR_Ns4RLw)
2. [Microsoft ML for Beginners Course](https://github.com/microsoft/ML-For-Beginners)
3. [Explore and analyze data with Python](https://learn.microsoft.com/en-us/training/modules/explore-analyze-data-with-python/?wt.mc_id=studentamb_271760)
