# UNESCO World Heritage Information Retrieval System

## Project Motivation

This project was inspired by the idea that such a system could be highly useful in travel scenarios. 
When planning a trip, users often want to explore globally recognized heritage sites in their destination country. 
This system helps users easily discover such sites by entering a country name or keywords related to the type of heritage they are interested in. 

The goal is to allow travelers to:
- Search for UNESCO World Heritage sites by country.
- Retrieve information based on descriptive queries (e.g., historical period, architectural style, etc.).
- Use the system as a helpful tool for travel planning and destination exploration.


This system can also serve as an educational tool.  
Students can use it to explore and learn about a wide range of UNESCO World Heritage sites around the world.  
By entering country names or descriptive queries, they can discover historical, cultural, and natural sites, making it useful for school projects, research, or general knowledge-building.

It encourages curiosity about global heritage and provides a hands-on way to interact with structured information.

## Dataset

To build this project, data was collected from the following sources:

- **1,224** UNESCO World Heritage sites:  
  [https://whc.unesco.org/en/list/](https://whc.unesco.org/en/list/)
  
- **72** Korea-related UNESCO-listed documents from the following four categories:
  - [Memory of the World](https://www.unesco.org/en/memory-world)
  - [Intangible Cultural Heritage](https://www.unesco.org/en/culture)
  - [Man and the Biosphere Programme (MAB)](https://www.unesco.org/en/mab/list?hub=66369)
  - [Global Geoparks](https://www.unesco.org/en/iggp/geoparks#full-list-of-unesco-global-geoparks)

These documents were either crawled programmatically or manually collected and stored as `.txt` files.

### Folder Structure inside `lsi_dataset/`

- **`Korea/`**  
  Contains datasets related to Korea's UNESCO-listed documents.

- **`saved_texts/`**  
  Contains the full dataset of UNESCO World Heritage site descriptions.  
  ⚠️ Due to file count limitations in some environments (1,000 files per folder), additional files are placed in the `saved_texts2/` folder.  
  Please move the contents of `saved_texts2/` into `saved_texts/` before running the program.

- **`test_dataset/`**  
  A small evaluation dataset containing 40 selected UNESCO World Heritage site files for testing purposes.

---

## Python Files Overview

Each search model and evaluation module is implemented as a standalone Python script with a `main` function, allowing them to be executed directly.

### Search Engine Modules

- **`boolean_model.py`**  
  Implements the Boolean search engine.

- **`vector_space.py`**  
  Implements the Vector Space Model search engine.

- **`lsi.py`**  
  Implements the Latent Semantic Indexing (LSI) search engine.

### Evaluation Modules

- **`boolean_evaluate.py`**  
  Uses functions from `boolean_model.py` to calculate precision, recall, and F1 score.

- **`vector_space_evaluate.py`**  
  Uses functions from `vector_space.py` to calculate precision, recall, and F1 score.

- **`lsi_evaluate.py`**  
  Uses functions from `lsi.py` to calculate precision, recall, and F1 score.

### Installation

Before running the LSI system, make sure to install the required Python packages:

```bash
pip install numpy scikit-learn
```

---

### Dataset Crawling

- **`lsi_dataset/crawling.py`**  
  Script used to crawl UNESCO World Heritage data from the official website and save it as `.txt` files.

