Installation
============

Follow these steps to install and run the **L7erf Bot** application:

---

### 1. Clone the Repository

Begin by cloning the official **L7erf Bot** repository from GitHub. Open a terminal and execute the following command:

.. code-block:: bash

   git clone https://github.com/BettyJk/L7erf.git

This will create a local copy of the repository on your machine.

---

### 2. Install Dependencies

Once you have cloned the repository, navigate to the project directory:

.. code-block:: bash

   cd L7erf

Next, install the necessary dependencies. The project relies on various Python libraries, which are listed in the `requirements.txt` file. Use the following command to install them:

.. code-block:: bash

   pip install -r requirements.txt

This will install all required packages, including those for machine learning, data processing, and user interface components.

---

### 3. Set Up Environment Variables (Optional)

Some of the components in **L7erf Bot**, such as the NLP models, may require environment variables or configuration files for optimal performance. Check the `.env.example` file for variables that might need to be configured (e.g., API keys or model paths).

If required, create a `.env` file in the root directory and fill in the necessary details.

---

### 4. Run the Application

Now that the repository is cloned and dependencies are installed, you can start the application. To run the **L7erf Bot** interface with Streamlit, execute the following command:

.. code-block:: bash

   streamlit run app.py

Streamlit will launch a local web server and display the application in your default web browser. The bot interface should now be accessible at `http://localhost:8501`.

---

### 5. Accessing the Application

Once the Streamlit server is up and running, you can interact with the **L7erf Bot**. The application includes various functionalities, including summarization, note organization, and more, depending on the modules you want to use.

- **Summarization**: The bot will process and summarize PDF documents.
- **ENSAM Information**: Interactive chatbot for exploring ENSAM Meknès academic programs and student life.
- **Course Q&A**: A specialized model fine-tuned on ENSAM-related content to help answer academic questions.

---

### Troubleshooting

If you encounter any issues during installation or running the application, refer to the **Troubleshooting** section of the documentation for common problems and solutions.

- **Problem 1**: Streamlit not starting – Make sure `streamlit` is installed correctly by running `pip show streamlit`.
- **Problem 2**: Missing dependencies – Ensure all dependencies from `requirements.txt` are successfully installed. Run `pip install --upgrade -r requirements.txt` to resolve issues.

---

### Additional Configuration

If you plan to run the application in a production environment, consider the following additional configurations:

- **Deployment**: You may deploy the application on cloud platforms such as AWS, Google Cloud, or Heroku. Refer to the deployment documentation for specific setup instructions.
- **Model Fine-Tuning**: If you intend to fine-tune the models further, refer to the fine-tuning section in the documentation for guidance on configuring your training environment.

---

By following these steps, you should be able to successfully set up and run the **L7erf Bot** on your machine. For additional support, please check the FAQ section or open an issue in the GitHub repository.
