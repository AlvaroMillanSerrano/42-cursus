import sys
from importlib import metadata


if __name__ == "__main__":
    print(
            "\nLOADING STATUS: Loading programs...",
            "\nChecking dependencies:",
            sep="\n"
        )
    libs: list[str] = ["pandas", "numpy", "matplotlib", "requests"]
    mising_libs: list[str] = []
    for lib in libs:
        try:
            version = metadata.version(lib)
        except Exception as e:
            mising_libs.append(e)
        else:
            print(f"[OK] {lib} ({version})")
    if mising_libs:
        for missing in mising_libs:   
            print(f"[ERROR] {missing}")
        print("\nInstallation with pip: pip install -r requirements.txt")
        print("Installation with poetry: poetry install")
        print("Running with poetry: poetry run python loading.py")
        print("[ADVICE] Use a venv to test pip and poetry")
        sys.exit(1)
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    print(
        "\nAnalyzing Matrix data...",
        "Processing 1000 data points...",
        sep="\n"
    )
    time = np.linspace(0, 10, 1000)
    matrix_signal = np.sin(time) + np.random.randn(1000)
    m_data = pd.DataFrame({'Time': time, 'Signal': matrix_signal})
    m_data['Smooth_Signal'] = m_data['Signal'].rolling(window=30).mean()
    print("Generating visualization...")
    plt.plot(
        m_data['Time'],
        m_data['Signal'],
        label='Matrix Data',
        alpha=0.5,
        color='gray'
    )
    plt.plot(
        m_data['Time'], m_data['Smooth_Signal'],
        label='Filtered Stream',
        color='green'
    )
    plt.title("Matrix Analysis")
    plt.xlabel("Time")
    plt.ylabel("Signal")
    plt.legend()
    plt.savefig('matrix_analysis.png')
    print(
        "\nAnalysis complete!",
        "Results saved to: matrix_analysis.png",
        sep="\n"
    )
