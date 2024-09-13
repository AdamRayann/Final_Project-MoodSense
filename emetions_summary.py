import matplotlib.pyplot as plt
import ast  # To safely evaluate the string to a dictionary

emotions = ["Angry", "Disgusted", "Fearful", "Happy", "Neutral", "Sad", "Surprised"]
emotion_dict = {emotion: 0 for index, emotion in enumerate(emotions)}


def emetions_summary(predicted_emotion):
    # Initialize with simple numeric labels (for example)
    if predicted_emotion in emotion_dict:
        emotion_dict[predicted_emotion] += 1
    # Print the dictionary to verify

def main(predicted_emotion):
    emetions_summary(predicted_emotion)

def get_summary():
    return emotion_dict

def plot_summary():
    '''# Plotting the data
    plt.figure(figsize=(10, 6))  # Set the figure size
    plt.bar(emotion_dict.keys(), emotion_dict.values(), color='skyblue')  # Create a bar chart
    plt.xlabel('Emotions')  # Label on X-axis
    plt.ylabel('Counts')  # Label on Y-axis
    plt.title('Emotion Distribution')  # Title of the plot
    plt.xticks(rotation=45)  # Rotate the X-axis labels for better readability
    plt.tight_layout()  # Adjust layout to make room for the rotated X-axis labels
    plt.show()  # Display the plot'''

    # Define colors for each emotion
    colors = ['red', 'green', 'blue', 'yellow', 'grey', 'purple', 'orange']

    # Plotting the bar chart
    plt.figure(figsize=(16, 7))  # Set the figure size
    plt.subplot(1, 2, 1)  # Specify this is the first of two plots
    plt.bar(emotion_dict.keys(), emotion_dict.values(), color='skyblue')  # Create a bar chart with colors
    plt.xlabel('Emotions')  # Label on X-axis
    plt.ylabel('Counts')  # Label on Y-axis
    plt.title('Emotion Distribution')  # Title of the plot
    plt.xticks(rotation=45)  # Rotate the X-axis labels for better readability

    # Plotting the pie chart
    plt.subplot(1, 2, 2)  # Specify this is the second of two plots
    total = sum(emotion_dict.values())
    percentages = [f'{(count / total * 100):.2f}%' for count in emotion_dict.values()]
    wedges, texts, autotexts = plt.pie(emotion_dict.values(), labels=percentages, colors=colors, startangle=90,
                                       counterclock=False, autopct='%1.1f%%')
    plt.title('Emotion Percentages')  # Title of the plot
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Adding legend
    plt.legend(wedges, emotion_dict.keys(), title="Emotions", loc="upper right", bbox_to_anchor=(1.3, 1))

    # Adjust layout and display
    plt.tight_layout()
    plt.show()







