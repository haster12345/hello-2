[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/8Gqy5HOm)
# ST207 - DATABASES: Assignment 2 (AT 2025)

### Overall objective

This assignment is intended to assess your knowledge of NoSQL database programming.

### Instructions (read carefully)

* The assignment comprises **two questions**, each worth 50% of the mark.
* You **must** write **one Python code (notebook) for each question**. Please, **DO NOT** submit one single file as your solutions will be assessed by different examiners.
* Make sure **your code files show the results for each cell**, especially those commands retrieving data from the database. You can export a PDF or HTML of your notebook and upload it along with your Python notebook.
* Remember that this is a **2-step submission process**: once you have all your files on GitHub, copy the link to your GitHub repository and submit it through Moodle ([Coursework submissions](https://moodle.lse.ac.uk/mod/assign/view.php?id=1836275) section). Avoid, as much as possible, any identifiable information (other than your candidate number) on your submitted work.

<hr> 

### Question 1: MongoDB

In this question, you will use the **Northwind** example database as a **collection of documents** to answer some questions.

1. Set up a MongoDB Atlas cluster.
2. Create a Python notebook with `PyMongo` installed, and connect it to your Atlas cluster.
3. Download the Northwind database (CSV files) from the [data](./data) folder. There are 6 files mapping categories, customers, employees, orders, products, and suppliers.
4. Have a look at the [Northwind Entity-Relationship model](./fig/Northwind_ER.png) to get a sense of existing entities, primary/foreign keys, and relationships. Notice that `Orders` and `Order_Details` were merged into one single file (`orders.csv`).
5. Answer the questions below in your Python notebook. 

1A) Create a new database (`db`) called `Northwind` and load each CSV file into a new collection (for instance, `customers.csv` into `db["customers"]`). **Important:** when loading the CSV files into documents, check for relationships (foreign keys) between entities (for instance, `products` and `suppliers`) and **manually create all relationships**, by mapping foreign keys into object IDs and/or embedding one document into another document. Write a short explanation (up to 3 paragraphs) on your report on which relationships are embedded and which ones are referenced using object IDs and why you decided for one or another approach.

1B) List all product names and unit prices supplied by each company (supplier), along with the supplier's name. The output should have one document per supplier, with the required information. 

1C) For each customer, list all the products they have purchased. The output should contain the customer information, along with a list of purchased products with product name, total quantity purchased, and total spent (computed from the list of products). 

1D) Create a materialised "view" collection `customer_sales_summary` with one document per customer and containing the total number of orders, total quantity purchased (sum of all products purchased across all orders), total revenue, list of unique product categories purchased, and first and most recent order dates. Ensure the result is stored as a materialised view collection.

<hr> 

### Question 2: Neo4j

In this question, you will build a graph database for **movie recommendation**.

1. Set up a Neo4j AuraDB cluster.
2. Create a Python notebook with a Neo4 driver installed, and connect it to your AuraDB cluster.
3. Download the [MovieLens 100K](https://grouplens.org/datasets/movielens/100k/) (`ml-100k.zip`) dataset. Relevant CSVs are: `u.user` (users), `u.item` (movies), `u.genre` (movie genres), `u.data` (user ratings), `u.occupation` (occupations with descriptions). This dataset contains: 943 users, 1682 movies, 5-star rating system, movies with genre indicators (binary flags). **Check the [README.txt](https://files.grouplens.org/datasets/movielens/ml-100k-README.txt) for more details**.
4. Answer the questions below:

2A.1) Design a Property Graph Data Model with nodes and relationships, considering:

* Nodes (and properties)
   * `User (userId, age, gender, occupation, zip code)`
   * `Movie (movieId, title, releaseYear)`
   * `Genre (name)`
   * `Occupation (name)`
   
* Relationships
   * an user provides a rating to a movie (and the database captures the timestamp of such rating)
   * a movie belongs to one or more genres
   * an user has an occupation
   * a movie is similar to another movie, based on computed genre overlap and co-ratings (see query 2D)

Feel free to adapt the above list of nodes and relationships to include any other relevant modelling decision. Explain your property graph data model on your report (up to 3 paragraphs), especially your decisions regarding nodes, relationships, and properties. **Upload a figure/diagram of your Property Graph Data Model along with your report**.

2A.2) Load the database

Populate your graph from the CSV files. **Note that the CSV files have no headers, so you need to add them before loading into the database (see README.txt mentioned above)**. Show all loading commands in your Python notebook, along with the final graph (you can use *yFiles*; see Seminar 9). Alternatively, you can upload a screenshot taken from your AuraDB instance along with your code. 

2B) Graph traversal

For a given user, recommend 10 movies they haven’t watched yet but are highly rated by similar users. The input can be a specific userId and the output should contain the movie title and the average rating, in descending order. You can decide the threshold for "highly rated" (**make sure to document this decision in your code and report**). 

2C) Pattern matching

Find "movie triangles" (triples of movies) with shared genres, where all movies share at least one genre and are connected through users who rated all three movies highly (for instance, `>4 stars`). You can decide the threshold for "highly rated" (**make sure to document this decision in your code and report**). The output should contain the genre and the titles of all three movies, for every triangle found. 

2D) Graph algorithm computation

Compute movie similarity via genre and actor overlap. We want to create or modify edges in the graph to capture similar movies based on shared genres or cast members. You can compute a `genreScore` based on the number of common genres between two movies, and an `actorScore` based on shared cast members between two movies, and then combine both scores into a `totalScore`. You *can* specific different weights for genre and actor to account for weak and strong similarity signals. You *need* to specify a threshold for `totalScore` (let's say, `>= 3`) to avoid generating similarity edges for nearly every pair of movies sharing one common element (genre or actor). You can run exploratory queries to identify how many movies share 2, 3, 4 or more genres or actors, and pick the threshold based on the percentage of movies sharing genres or actors, so you can find a good compromise. You may note that most movies share at least one genre; thus, having a proper threshold helps to control graph density and filter out noisy edges. **Your code must show all the queries used to compute movie similarity, along with proper explanation**. At the end, we want to database to have relationships like `(:Title)-[:SIMILAR_TO {totalScore: …}]->(:Title)`. **You should add or modify these relationships in your database and show at least 3 of them in your code**. 

<hr>

## Key dates
* Assignment release: 28/11/2025, 5 pm
* Solution deadline: 12/12/2025, 5 pm (both GitHub and Moodle)
* Feedback and provisional marks: 09/01/2026, 8 pm
* Requests for extension: see corresponding section below.
* **Any requests for extensions will cause all provisional marks and feedback to be held until all submissions are completed!**

<hr>

### Assessment criteria

See [AssessmentCriteria.pdf](./AssessmentCriteria.pdf).

<hr>

## Database tools

You can use MongoDB and Neo4j tools, both Web and desktop versions, to help you visualise the database and prototype/test any queries. However, **all final queries must be incorporated in your Python notebooks**.

<hr>

## Generative AI tools

As per School and course-specific policy, you may acknowledge the use of any generative AI tool in any part of your summative work. You may note that marks can be deducted if no acknowledgement is made and/or a substantial part of your work (especially coding) is done by these tools. See [Moodle](https://moodle.lse.ac.uk/course/view.php?id=14082) for guidance.

You may use these tools literally as an "assistant" and “co-pilot” to help you prototype your database models, generate synthetic data, and/or structure your SQL queries, but the final results must be your own, validated work.

<hr>

## Deliverables

**Remember to NOT include any identifiable information on your submission. Use your candidate number whenever necessary.**

* **Source files (Python notebooks) for both questions (MongoDB and Neo4j), including 1A-1D and 2A.2-2D**. Make sure both code files show all outputs. You can export them as PDF or HTML files. **See Database tools**.
* **Chat logs** exported from generative AI tools (if any).
* **Figure or screenshot of your Property Graph Data Model (2A.1)**.
* **Figure or screenshot of your final graph database (2A.2)**. Note that AuraDB allows you to visualise the graph and a summary, coloured tab with the number of nodes, properties, and relationships. You can take a screenshot of such summary tab as well.
* **PDF report** (up to 5 pages, excluding references) with the following structure:
  * your candidate number at the top of the document.
  * short explanation (up to 3 paragraphs) of your MongoDB database, including which relationships are embedded and which ones are referenced using object IDs and why you decided for one or another approach.
  * short explanation of each query (1B-1D).
  * short explanation (up to 3 paragraphs) of your Property Graph Data Model, especially your decisions regarding nodes, relationships, and properties, along with a figure/diagram of your model (question 2A.1).
  * there's no need to comment on question 2A.2, provided your code shows all data loading commands and respective outputs.
  * short explanation of each query (2B-2D), including decisions about thresholds and other assumptions and parameters used in your code. Pay attention to query 2D as it requires a few more discussion in the report.
  * **there's no need to include outputs, as your code files must show them**.
  * A **statement on the use of any generative AI tools**, as per School and course-specific policies. See [Moodle](https://moodle.lse.ac.uk/course/view.php?id=14082) for guidance.

<hr>

## Submission

This a 2-step (GitHub and Moodle) submission process:

* All files should be uploaded into your `assignment2` repository on GitHub. Observe that GitHub has a limit on the size of each file (see [here](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)). If you have any large files, include in your report a link to an external repository (for instance, Google Drive, Dropbox, WeTransfer) and make sure the file is accessible for download.
* **DO NOT use any other GitHub repository**, as we won’t track your submission, and this will cause delays in assessing your work and providing feedback and provisional marks. When you are ready to submit, **remove any unnecessary files** on your `assignment2` repository – keep only the relevant deliverables.
* Copy the URL address of your GitHub repository, go to the submission portal on Moodle and paste it or include it on a text file. **Make sure to press Submit to complete your assignment submission**.
* **These two steps must be done by the deadline.**

<hr>

## Extension requests

You have the right to ask for an extension under some circumstances, as per LSE Extension Policy. Check [here](https://info.lse.ac.uk/current-students/services/assessment-and-results/exceptional-circumstances/extension-policy) for guidance and the necessary documents. **Please note that any extensions must be requested and approved before the deadline, so do not leave this to the last minute as it may incur late penalties being applied to your work**. You should submit your requests to Dr. Christine Yuen (BSc Data Science programme director) and Lai Ching To (Sharon) (Undergraduate Programmes Administrator) for analysis. See [here](https://www.lse.ac.uk/statistics/people) for contact details, under Academic Faculty and Professional Service Staff, respectively. If you have adjustments in place and need an extension, follow the same procedure and contact your teachers for advice.

<hr>

## Feedback and provisional marks

Feedback and provisional marks will be provided in a markdown (.md) file in your “assignment2” repository by the expected date. Please, note that we do our best to provide you with relevant and meaningful feedback by the intended deadline, but **we reserve the right to delay any feedback while any extension requests are in place. You may also note that all marks are provisional and subject to changes to comply with School and departmental policies on mark distributions and as a result of external examiners and sub-board revisions**.

<hr>

## TODO
- [x] link users and occupations
- [x] Q 2C
- [x] Q 2D


