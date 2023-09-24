import sys
import time

from modules.connection import Connection
from modules.iidx import iidx_ticker_get

host = "localhost"
port = 1999
password = "" 

def main():
    # Create a connection to the server
    connection = Connection(host, port, password)

    try:
        while True:
            # Get the ticker text
            ticker_text = iidx_ticker_get(connection)

            # Check if ticker_text is a list and not empty
            if isinstance(ticker_text, list) and ticker_text:
                # Access the first element and remove leading/trailing spaces and brackets
                ticker_text = ticker_text[0].strip("[]' ")

                # Split the text into segments of a fixed length (e.g., 16 characters)
                segment_length = 16
                segments = [ticker_text[i:i + segment_length] for i in range(0, len(ticker_text), segment_length)]

                # Display each segment sequentially
                for segment in segments:
                    # Print the ticker text segment
                    print(segment)

                    # Enabling pauses will break ticker sync with the game so eughhh not suggested
                    # time.sleep(1)
                    # by break i mean literally, this is how the "SELECT FROM SCRATCH RECOMMEND CATEGORY" text looks like with 2 seconds of pause:
                    # SELECT FR
                    # ECT FROM
                    # FROM SCR
                    # OM SCRATC
                    # SCRATCH R
                    # ATCH RECO
                    # H RECOMME
                    # ECOMMEND
                    # MMEND CAT
                    # D CATEGOR
                    # Y  SELECT 
            else:
                print("Invalid ticker text format")

    except Exception as e:
        print("Error:", e)
    finally:
        # Close the connection
        connection.close()

if __name__ == "__main__":
    main()
