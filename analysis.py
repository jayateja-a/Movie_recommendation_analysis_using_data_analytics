import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data = pd.read_csv('final_final_dataset.csv')

# Drop rows with missing values
data = data.dropna()

# Ensure correct data types
data['year'] = data['year'].astype(int)
data['revenue'] = data['revenue'].astype(float)
data['rating'] = data['rating'].astype(float)

# Frequency Table: Genres
genre_counts = data['genres'].str.split('|').explode().value_counts()
# print("Genre Frequency Table:\n", genre_counts)

# Bar Chart: Genres
plt.figure(figsize=(10, 6))
genre_counts.head(10).plot(kind='bar', color='skyblue')
plt.title('Top 10 Most Frequent Genres')
plt.xlabel('Genre')
plt.ylabel('Count')
plt.show()


# Revenue by Genre
genre_revenue = data.groupby('genres')['revenue'].mean().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
genre_revenue.head(10).plot(kind='bar', color='green')
plt.title('Average Revenue by Genre')
plt.xlabel('Genre')
plt.ylabel('Average Revenue')
plt.show()

# Director Success by Revenue
director_revenue = data.groupby('director')['revenue'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
director_revenue.plot(kind='bar', color='purple')
plt.title('Top 10 Directors by Revenue')
plt.xlabel('Director')
plt.ylabel('Total Revenue')
plt.show()

# Year-Wise Performance (Rating and Revenue)
yearly_rating = data.groupby('year')['rating'].mean()
yearly_revenue = data.groupby('year')['revenue'].sum()

plt.figure(figsize=(12, 6))
plt.plot(yearly_rating, marker='o', label='Average Rating', color='blue')
plt.plot(yearly_revenue / 1e9, marker='s', label='Total Revenue (in Billion $)', color='red')
plt.title('Year-Wise Performance (Rating & Revenue)')
plt.xlabel('Year')
plt.ylabel('Value')
plt.legend()
plt.show()

# Does Rating Impact Revenue? (Scatter Plot)
plt.figure(figsize=(10, 6))
sns.scatterplot(x='rating', y='revenue', data=data, alpha=0.7, color='darkblue')
plt.title('Does Rating Impact Revenue?')
plt.xlabel('Rating')
plt.ylabel('Revenue')
plt.show()

# Top Movies Each Year by Rating
top_movies_by_rating = data.loc[data.groupby('year')['rating'].idxmax()][['year', 'movie', 'rating']]
print("Top Movies by Rating Each Year:\n", top_movies_by_rating)

# Top Movies Each Year by Revenue
top_movies_by_revenue = data.loc[data.groupby('year')['revenue'].idxmax()][['year', 'movie', 'revenue']]
print("Top Movies by Revenue Each Year:\n", top_movies_by_revenue)


import seaborn as sns
import matplotlib.pyplot as plt

# Select numerical columns for correlation analysis
numerical_columns = ['rating', 'revenue', 'duration', 'year']
correlation_matrix = data[numerical_columns].corr()

# Plot the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap of Numerical Variables")
plt.show()


# Group data by year and sum revenue
yearly_revenue = data.groupby('year')['revenue'].sum()

# Line plot of revenue trends
plt.figure(figsize=(12, 6))
sns.lineplot(x=yearly_revenue.index, y=yearly_revenue.values, marker="o", color="blue")
plt.title("Yearly Total Revenue Trends")
plt.xlabel("Year")
plt.ylabel("Revenue (in billions)")
plt.grid(True)
plt.show()


# Box plot of movie duration vs. rating
plt.figure(figsize=(10, 6))
sns.boxplot(data=data, x=pd.cut(data['duration'], bins=[0, 90, 120, 150, 300], labels=['<90 min', '90-120 min', '120-150 min', '>150 min']), y='rating')
plt.title("Impact of Movie Duration on Ratings")
plt.xlabel("Movie Duration")
plt.ylabel("Rating")
plt.show()
