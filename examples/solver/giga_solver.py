import argparse

from mangas.solvers import GigaPuzzleSolver


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str)
    parser.add_argument("--output", "-o", type=str)
    return parser.parse_args()


def main():
    args = parse_args()

    solver = GigaPuzzleSolver()

    image = solver.solve_from_url(args.url)

    if args.output:
        image.to_pil().save(args.output)
    else:
        image.to_pil().show()


if __name__ == "__main__":
    main()
