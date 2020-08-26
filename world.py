import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# grid values
ON = 255
OFF = 0
vals = [ON, OFF]

# build empty grid
def build_grid(N):
    print('Building grid')
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

# apply rules to current grid and update
def update(frameNum, img, grid, N):
    # copy grid for calculation
    newGrid = grid.copy()

    # loop through every pixel
    for i in range(N):
        for j in range(N):
            neighborCount = count_neighbors(grid, i, j, N)

            # apply rules
            if grid[i, j] == ON and (neighborCount < 2 or neighborCount > 3):
                newGrid[i, j] = OFF
            elif grid[i, j] == OFF and neighborCount == 3:
                newGrid[i, j] = ON

    # update the grid
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# display the grid
def show_grid(grid, N, interval):
    print('Showing grid')

    # setup animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                    frames = 10,
                                    interval = interval,
                                    save_count = 50)

    plt.show()

# count the number of neighbors at location
def count_neighbors(grid, i, j, N):
    return (grid[(i-1)%N, (j-1)%N] + grid[i, (j-1)%N] + grid[(i+1)%N, (j-1)%N] +
        grid[(i-1)%N, j] + grid[(i+1)%N, j] +
        grid[(i-1)%N, (j+1)%N] + grid[i, (j+1)%N] + grid[(i+1)%N, (j+1)%N]) / 255

def main():
    print("Welcome to Conway's World!")

    # setup command line parser
    argParser = argparse.ArgumentParser(description = "Conway's Game of Life")

    # setup possible args
    argParser.add_argument('--grid-size', dest = 'N', required = False)
    argParser.add_argument('--interval', dest = 'interval', required = False)

    # get args
    args = argParser.parse_args()

    # set grid size ; default to 32
    N = 32
    if args.N and int(args.N) > 8:
        N = int(args.N)

    print('N: ' + str(N))

    # set update interval ; default to 50 ms
    interval = 50
    if args.interval:
        interval = int(args.interval)

    print('interval: ' + str(interval) + ' ms')

    # build empty grid
    grid = build_grid(N)

    # show the grid
    show_grid(grid, N, interval)

if __name__ == '__main__':
    main()
