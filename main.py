import argparse

import pandas as pd
import matplotlib.pyplot as plt


def process_data(df):
    df = df[df['Date of Final Decision'].notna()]
    df['Date of Final Decision'] = pd.to_datetime(df['Date of Final Decision'], format='%m/%d/%Y', errors='coerce')
    df = df.dropna(subset=['Date of Final Decision'])
    df['Year'] = df['Date of Final Decision'].dt.year
    submission_counts = df.groupby(['Year', 'Panel (lead)']).size().unstack(fill_value=0)
    return submission_counts.sort_index()


def generate_plot(submission_counts):
    fig, ax = plt.subplots(figsize=(12, 7))
    submission_counts.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
    ax.set_title('Number of 510(k) Submissions per Year by Panel', fontsize=16)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Submissions', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title='Panel', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    return fig


def main():
    parser = argparse.ArgumentParser(description='Process 510(k) submission data and generate a graph.')
    parser.add_argument('input_file', help='Path to the input CSV file')
    parser.add_argument('output_file', help='Path for the output graph image')
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.input_file)
        submission_counts = process_data(df)
        fig = generate_plot(submission_counts)
        fig.savefig(args.output_file, dpi=300, bbox_inches='tight')
        print(f"Graph saved as {args.output_file}")
    except FileNotFoundError:
        print(f"Error: The input file '{args.input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()