


def NMSE(w, h, img, enc):
    numerator = 0
    denominator = 0

    for i in range(w):
        for j in range(h):
            numerator+= (
                    (
                            sum(img[i, j]) + sum(enc[i, j])
                    )**2
            )
            denominator+=(sum(img[i, j])**2)
    return numerator/denominator

def MSE(w, h, img, enc):
    numerator = 0


    for i in range(w):
        for j in range(h):
            numerator += (
                    (
                            sum(img[i, j]) + sum(enc[i, j])
                    ) ** 2
            )

    return numerator / (h*w)

def LMSE(w, h, img, enc):
    def d_q(i, j, im):
        return sum(im[i+1,j])+sum(im[i,j+1])+sum(im[i-1,j])+sum(im[i,j-1])-4*sum(im[i,j])

    numerator = 0
    denominator = 0
    for i in range(1,w-1,1):
        for j in range(1,h-1,1):
            numerator+=(d_q(i, j, img)-d_q(i, j, enc))**2
            denominator+=d_q(i, j, img)**2
    return numerator/denominator

