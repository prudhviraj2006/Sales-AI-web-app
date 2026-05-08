import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import os

def test_chart():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    ax.set_title("Matplotlib Test Chart")
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    print(f"Chart generated successfully. Size: {len(buf.getvalue())} bytes")

if __name__ == "__main__":
    test_chart()
