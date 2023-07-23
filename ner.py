import spacy
from collections import defaultdict
from spacy.matcher import PhraseMatcher


class NER:
    def __init__(self):
        """
        Initialize the Named Entity Recognition (NER) class.

        Loads the SpaCy language model, initializes the PhraseMatcher for special place names,
        and defines the special place names to search for.
        """

        self.nlp = spacy.load("en_core_web_lg")
        self.phrase_matcher = PhraseMatcher(self.nlp.vocab)

        # Define the special place names as phrases
        self.special_place_names = [
            "United States of America",
            "THE UNITED STATES",
            "GARDEN CITY",
        ]

        # Add the special place names to the phrase matcher
        patterns = [self.nlp(name) for name in self.special_place_names]
        self.phrase_matcher.add("SPECIAL_PLACES", None, *patterns)

    def process_text(self, text):
        """
        Process the input text to extract named entities and associated places.

        Args:
            text (str): The input text to be processed.

        Returns:
            tuple: A tuple containing two defaultdicts.
                - The first defaultdict stores the names of people as keys and their respective counts as values.
                - The second defaultdict stores the names of people as outer keys, and their associated places as inner keys along with their respective counts.
        """

        N = 100
        text = text.replace("\r\n", " ")  # Replace special characters
        doc = self.nlp(text)

        person_names = defaultdict(int)  # Use defaultdict to store name counts
        person_places = defaultdict(
            lambda: defaultdict(int)
        )  # Store places associated with each person

        for entity in doc.ents:
            if entity.label_ == "PERSON":
                if all(char.isalpha() or char.isspace() for char in entity.text):
                    person_names[entity.text] += 1
                    person_start = entity.start
                    person_end = entity.end

                    # Search for associated places within N words either side of the person's name
                    for i in range(
                        max(0, person_start - N), min(len(doc), person_end + N)
                    ):
                        if doc[i].ent_type_ == "GPE":
                            person_places[entity.text][doc[i].text] += 1

        # Search for special place names using the phrase matcher
        special_place_matches = self.phrase_matcher(doc)
        for match_id, start, end in special_place_matches:
            place_name = doc[start:end].text
            for name in person_places:
                if name in text and place_name in text:
                    person_places[name][place_name] += text.count(place_name)

        return person_names, person_places
