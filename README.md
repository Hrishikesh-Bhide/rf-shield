# rf-shield

# RF Shield

RF Shield is a project developed with the aim of empowering individuals to make informed decisions about their living environment concerning potential health risks associated with RF radiation exposure from nearby communication towers. The project offers various functionalities, including identifying RF-Shielded and RF-Exposed areas, displaying cellular tower locations on maps, providing news updates on relevant issues, and more.

## Table of Contents
- [Getting Started](#getting-started)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [How to Use](#how-to-use)
- [Challenges Faced](#challenges-faced)
- [What We Learned](#what-we-learned)
- [Accomplishments](#accomplishments)
- [Future Enhancements](#future-enhancements)
- [Conclusion](#conclusion)

## Getting Started

To get started with RF Shield, follow these steps:
1. Clone the repository to your local machine.
2. Install the necessary dependencies.
3. Run the application.

## Features

RF Shield offers the following features:

1. **Cellular Tower Locations:** View cellular tower locations on a map represented by red circles.
2. **Cellular Towers Proximity:** Display a map highlighting all cellular towers in the vicinity.
3. **Locational Mapping and Radius Highlighting:** Target entered addresses and delineate circular areas based on scientific measurements to determine RF exposure.
4. **Identify RF-Shielded/RF-Exposed Area:** Indicate whether the entered address falls within an RF-Shielded or RF-Exposed area.
5. **Color-Coded Representation:** Designate RF-Shielded areas with a blue circular border and RF-Exposed areas with a red border.
6. **Latest Trending News:** Provide the top 5 most relevant articles to keep users informed about developments in their area regarding cellular towers or related news.

## Technologies Used

The project utilizes the following technologies:

- Python
- Streamlit
- Folium
- Geodesic
- Nominatim
- Beautiful Soup
- Google Gemini Pro LLM
- AWS (deployment)

## How to Use

1. Input your address.
2. Explore the provided information regarding RF exposure and nearby cellular towers.
3. Stay informed about relevant news articles related to cellular tower developments.

## Challenges Faced

Some challenges encountered during the development of RF Shield include:

- Initial limitations with map functionality led to the exploration of alternative libraries like Folium.
- Ensuring accuracy and completeness of tower dataset.
- Optimizing geospatial calculations for real-time analysis.
- Fine-tuning the NLP model for article summarization.
- Setting up deployment on AWS and resolving SSH and API key issues.

## What We Learned

Our journey with RF Shield provided valuable insights, including:

- Importance of user-centric development.
- Data-driven decision-making for safety recommendations.
- Integration of maps into Streamlit.
- Collaboration and innovation in addressing real-world issues.

## Accomplishments

RF Shield is proud to offer:

- Safety-centric approach prioritizing population well-being.
- Empowerment of users with tools for informed decision-making.
- Proactive measures for identifying potential danger zones.
- Promotion of awareness regarding health risks and safety measures.
- Potential positive impact on local communities and industries.

## Future Enhancements

Future enhancements for RF Shield include:

- Color-coded maps based on tower proximity.
- Development of a mobile app for on-the-go safety information.
- Real-time alerts for cellular tower registrations.
- Guidelines for raising objections to tower registrations.

## Conclusion

RF Shield reflects our commitment to leveraging technology for societal betterment. By providing actionable insights into RF radiation exposure and government initiatives, we aim to empower individuals to safeguard their health and well-being. As we continue to iterate and improve RF Shield, we look forward to making a meaningful impact on public awareness and safety.
