Installation
============

Follow these steps to install and run the **L7erf Bot** application on your local machine.

---

1. Clone the Repository
------------------------

To begin, clone the official **L7erf Bot** repository from GitHub. Open a terminal and execute the following command:

.. code-block:: bash

   git clone https://github.com/BettyJk/chatbotensam

This command creates a local copy of the repository on your machine. Once cloned, navigate to the project directory:

.. code-block:: bash

   cd chatbotensam

---

2. Install Dependencies
------------------------

The project relies on several Python libraries listed in the `requirements.txt` file. To install these dependencies, use the following command:

.. code-block:: bash

   pip install -r requirements.txt

**Tip**: It is recommended to use a virtual environment to avoid conflicts with existing Python packages. To set up a virtual environment, run:

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows

Then proceed with the dependency installation.

---

3. Set Up Environment Variables
-------------------------------

Certain features of **L7erf Bot**, such as NLP models or API integrations, may require environment variables. The repository includes a `.env.example` file with placeholders for necessary configurations like API keys and file paths.

**Steps:**

1. Copy the `.env.example` file and rename it to `.env`:

   .. code-block:: bash

      cp .env.example .env

2. Open the `.env` file and fill in the required details, such as:
   - API keys for external services.
   - Paths to pre-trained NLP models if applicable.

3. Save the file and ensure the application can access these variables.

---

4. Run the Application
----------------------

With dependencies installed and environment variables set, you’re ready to launch the **L7erf Bot**. Use the following command to start the Streamlit application:

.. code-block:: bash

   streamlit run chatbot.py

This command launches a local web server, and the application interface will open in your default web browser. You can access the bot at:

   http://localhost:8501

---

5. Using L7erf Bot
------------------

Once the application is running, you can explore its various features:

- **📄 Document Summarization**: Upload PDF files for automatic summarization.
- **🎓 ENSAM Information**: Interact with the bot to learn about ENSAM Meknès programs, schedules, and more.
- **🤖 Academic Q&A**: Use the chatbot to get answers to academic and course-related questions.

The intuitive interface ensures you can quickly access and utilize these features.

---

6. Access the Deployed Application
-----------------------------------

The **L7erf Bot** is also deployed and accessible via the following link:

   `Deployed App <https://chatbotensam-bettyhajar.streamlit.app>`_

**Note**: The deployed app may experience issues due to version conflicts. The team is actively working to resolve these problems for a smoother user experience.

---

7. Troubleshooting
-------------------

Encountered an issue? Below are solutions to common problems:

- **Streamlit not starting**: Ensure `streamlit` is correctly installed. Check its presence with:

   .. code-block:: bash

      pip show streamlit

   If not installed, run:

   .. code-block:: bash

      pip install streamlit

- **Dependency errors**: Double-check the installation of packages. Upgrade outdated or missing dependencies with:

   .. code-block:: bash

      pip install --upgrade -r requirements.txt

- **Environment variable issues**: Verify that the `.env` file is properly configured and matches the required format.

---

8. Explanatory Video
-------------------

To better understand how to use the **L7erf Bot**, refer to the following demonstration video:

.. raw:: html

   <video width="640" height="360" controls>
       <source src="howtouse.mp4 type="video/mp4">
       Your browser does not support the video tag.
   </video>

The video provides a step-by-step explanation of interacting with the bot and utilizing its features.

---

Next Steps
----------

Congratulations! You’ve successfully installed and launched the **L7erf Bot**. Dive into the application to explore its features, or proceed to the **Usage** section for detailed instructions on leveraging the bot’s capabilities.

For support or feedback, consult the FAQ section or submit an issue on the `GitHub repository <https://github.com/BettyJk/chatbotensam>`_.
