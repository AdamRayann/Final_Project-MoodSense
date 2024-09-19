import matplotlib.pyplot as plt
import time  # For generating timestamps

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
    # Generate a unique name for each image using the current timestamp
    timestamp = time.strftime("%H%M%S")  # Get current time as a string
    save_path = f'./summary/{timestamp}.png'  # Create the file name with the timestamp

    # Define colors for each emotion
    colors = ['red', 'green', 'blue', 'yellow', 'grey', 'purple', 'orange']

    # Create the figure and plot both bar chart and pie chart
    plt.figure(figsize=(16, 7))

    # Bar chart
    plt.subplot(1, 2, 1)
    plt.bar(emotion_dict.keys(), emotion_dict.values(), color='skyblue')
    plt.xlabel('Emotions')
    plt.ylabel('Counts')
    plt.title('Emotion Distribution')
    plt.xticks(rotation=45)

    # Pie chart
    plt.subplot(1, 2, 2)
    total = sum(emotion_dict.values())
    percentages = [f'{(count / total * 100):.2f}%' for count in emotion_dict.values()]
    wedges, texts, autotexts = plt.pie(emotion_dict.values(), labels=percentages, colors=colors, startangle=90,
                                       counterclock=False, autopct='%1.1f%%')
    plt.title('Emotion Percentages')
    plt.axis('equal')

    # Adding legend
    plt.legend(wedges, emotion_dict.keys(), title="Emotions", loc="upper right", bbox_to_anchor=(1.3, 1))

    # Save the figure as an image file
    plt.tight_layout()
    plt.savefig(save_path)  # Save the figure to the unique path

    # Optionally close the plot to free up memory
    plt.close()

    # Return the path to the saved image
    return save_path








