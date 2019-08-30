import numpy as np

"""Module containing all we need for the pacman board.

Technical details:
    -A pacman board consists of 36x28 (height x width) tiles, each of which being an
        8x8 pixel square. Most of these tiles are inaccessible to the pacman and the ghosts.
    -A piece is considered to live in the tile its centre falls in. Two pieces have collided
        if they occupy the same tile.
    -The 'ghost house' is a special region of the board the pac can never enter, and ghosts
        can only enter under specific circumstances.

"""

class board:
    #We order our columns from left to right and rows from bottom to top of our
    #pacman grid, which means the corner listing below goes from bottom to top and
    #fills across the board.

    #The connections matrix stores data about how each vertex is connected to every
    #other vetex. We need only work out the first half, because after that we may
    #transpose.
    #tpcm stancds for traditional pacman connection matrix!
    def create_connection_matrix(self):
        tpcm = np.zeros((len(self.corners),len(self.corners)))
        for i in range(len(self.corners)):
            tpcm[i,i] = 1
        tpcm[0,1], tpcm[0,4] = 1, 1
        tpcm[1,2], tpcm[1,8] = 1, 1
        tpcm[2,3], tpcm[2,9] = 1, 1
        tpcm[3,13] = 1
        tpcm[4,5] = 1
        tpcm[5,6], tpcm[5,15] = 1, 1
        tpcm[6,16] = 1
        tpcm[7,8], tpcm[7,17] = 1, 1
        tpcm[9,10] = 1
        tpcm[10,20] = 1
        tpcm[11,12], tpcm[11,21] = 1, 1
        tpcm[12,13], tpcm[12,22] = 1, 1
        tpcm[14,15], tpcm[14,24] = 1, 1
        tpcm[16,17], tpcm[16,25] = 1, 1
        tpcm[17,18] = 1
        tpcm[18,19], tpcm[18, 27] = 1, 1
        tpcm[19,20], tpcm[19,28] = 1, 1
        tpcm[20,21] = 1
        tpcm[21,30] = 1
        tpcm[22,23] = 1
        tpcm[23,31] = 1
        tpcm[24,25] = 1
        tpcm[25,26] , tpcm[25,34] = 1, 1
        tpcm[26,27], tpcm[26,32] = 1, 1
        tpcm[28,29] = 1
        tpcm[29,30], tpcm[29,33] = 1, 1
        tpcm[30,31], tpcm[30,37] = 1, 1
        tpcm[32,35], tpcm[32,33] = 1, 1
        tpcm[33,36] = 1
        tpcm[34,35], tpcm[34, 37], tpcm[34,43] = 1, 2, 1
        tpcm[35,38] = 1
        tpcm[36,37], tpcm[36,41] = 1, 1
        tpcm[37,48] = 1
        tpcm[38,39] = 1
        tpcm[39,40], tpcm[39,45] = 1, 1
        tpcm[40,46], tpcm[40,41] = 1, 1
        tpcm[42,43], tpcm[42,50] = 1, 1
        tpcm[43,51] = 1
        tpcm[44,45], tpcm[44,52] = 1, 1
        tpcm[46,47] = 1
        tpcm[47,55] = 1
        tpcm[48,56], tpcm[48,49] = 1, 1
        tpcm[49,57] = 1
        tpcm[50,51], tpcm[50,58] = 1, 1
        tpcm[51,52], tpcm[51,59] = 1, 1
        tpcm[52,53] = 1
        tpcm[53,60], tpcm[53,54] = 1, 1
        tpcm[54,55], tpcm[54,61] = 1, 1
        tpcm[55,56] = 1
        tpcm[56,57], tpcm[56,62] = 1, 1
        tpcm[57,63] = 1
        tpcm[58,59] = 1
        tpcm[59,60] = 1
        tpcm[61,62] = 1
        tpcm[62,63] = 1

        if self.grid_type == "pellet_grid":
            for i in range(32,42):
                tpcm[i,i] =0

            tpcm[18,19] = 0
            tpcm[26,32] = 0
            tpcm[29,33] = 0
            tpcm[32,33], tpcm[32,35] = 0, 0
            tpcm[33,36] = 0
            tpcm[34,37], tpcm[34,35] = 0, 0
            tpcm[35,38] = 0
            tpcm[36,37], tpcm[36,41] = 0, 0
            tpcm[38,39] = 0
            tpcm[39,45], tpcm[39,40] = 0, 0
            tpcm[40,41], tpcm[40,46] = 0, 0

        #although not neccessary, we do the transpose for completeness:
        for i in range(tpcm.shape[0]):
            for j in range(i, tpcm.shape[1]):
                tpcm[j][i] = tpcm[i][j]

        self.connection_matrix = tpcm

    def create_corners(self):
        self.corners = [[3,1], [3,12], [3,15], [3,26],
                [6,1], [6,3], [6,6], [6,9], [6,12], [6, 15], [6,18], [6,21], [6,24], [6,26],
                [9,1], [9,3], [9,6], [9,9], [9,12], [9, 15], [9,18], [9,21], [9,24], [9,26],
                [12,1], [12,6], [12,9], [12,12], [12, 15], [12,18], [12,21], [12,26],
                [15,9], [15,18],
                [18,6], [18,9], [18,18], [18,21],
                [21,9], [21,12], [21,15], [21,18],
                [24,1], [24,6], [24,9], [24,12], [24, 15], [24,18], [24,21], [24,26],
                [27,1], [27,6], [27,9], [27,12], [27, 15], [27,18], [27,21], [27,26],
                [31,1], [31,6], [31,12], [31,15], [31,21], [31,26]]

        #if self.grid_type == "ghost_grid":
    #        extra_corners = [[21,13], [21,14], [17,11], [17,12], [17,13], [17,14], [17,15], [17,16],
    #            [19,11], [19,12], [19,15], [19,16]]
    #        self.corners.extend(extra_corners)

    def __init__(self, size = (36*8, 28*8), grid_type = "pac_grid"):
        self.grid = np.zeros((36,28))
        self.grid_type = grid_type
        self.create_corners()
        self.create_connection_matrix()
        self.complete_grid()
        self.size = size
        self.grid_square_height = self.size[0]/self.grid.shape[0]
        self.grid_square_width = self.size[1]/self.grid.shape[1]

    def connect_corners(self, corner_1, corner_2, type=0):
        #(0 is not connected, 1 is an 'inside connection',
        #2 is 'outside' which goes across the edge of the board.)
        if corner_1[0] == corner_2[0] and corner_1[1] == corner_2[1]:
            if type != 0:
                self.grid[corner_1[0], corner_1[1]] = 1
        elif type == 1:
            if corner_1[0] == corner_2[0]:
                if corner_1[1] < corner_2[1]:
                    for j in range(corner_1[1], corner_2[1]+1):
                        self.grid[corner_1[0], j] = 1
                else:
                    self.connect_corners(corner_2,corner_1, type)
            elif corner_1[1] == corner_2[1]:
                if corner_1[0] < corner_2[0]:
                    for i in range(corner_1[0], corner_2[0]+1):
                        self.grid[i, corner_1[1]] = 1
                else:
                    self.connect_corners(corner_2, corner_1, type)
        elif type == 2:
            if corner_1[0] == corner_2[0]:
                if corner_1[1] < corner_2[1]:
                    for j in range(0,28):
                        if j not in range(corner_1[1], corner_2[1]+1):
                            self.grid[corner_1[0], j] = 1
                else:
                    self.connect_corners(corner_2, corner_1, type)
            elif corner_1[1] == corner_2[1]:
                if corner_1[0] < corner_2[0]:
                    for i in range(0,36):
                        if i not in range(corner_1[0], corner_2[0]+1):
                            self.grid[i, corner_1[1]] = 1
                else:
                    self.connect_corners(corner_1, corner_2, type)

    def complete_grid(self):
        for i in range(self.connection_matrix.shape[0]):
            for j in range(i, self.connection_matrix.shape[1]):
                self.connect_corners(self.corners[i], self.corners[j], self.connection_matrix[i][j])
