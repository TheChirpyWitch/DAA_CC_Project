#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "netpbm.h"
#include <stdio.h>
#include <time.h>
#include "uthash.h"

// double l[20000];
// int counter = 1; 

/* A dictionary (KEY, VALUE) with 
- KEY: label
- VALUE: RGBI values corresponding to that label
*/

struct label_colors {
    int label;                    /* key */
    int r, g, b, i;
    UT_hash_handle hh;         /* makes this structure hashable */
};

struct label_colors *labels = NULL; // my label-color hashtable

void add_label_color(int label, int r, int g, int b, int i) {
    struct label_colors *s;

    s = malloc(sizeof(struct label_colors));
    s->label = label;
    s->r = r;
    s->g = g;
    s->b = b;
    s->i = i;
    HASH_ADD_INT( labels, label, s );  /* id: name of key field */
    
}

struct label_colors *find_label_color(int label) {
    struct label_colors *s;

    HASH_FIND_INT( labels, &label, s);  /* s: output pointer */
    return s;
}







/* A dictionary (KEY, VALUE) with 
- KEY: label
- VALUE: a list of equivalent labels (PARENT LABEL)
*/

struct label_equivalence {
    int label;                    /* key */
    int *parent;
    int count;
    int visited;
    int size;
    UT_hash_handle hh;         /* makes this structure hashable */
};

struct label_equivalence *label_parents = NULL; // my label-label equivalence table

void add_parent_label(int label, int parent_label) {
    struct label_equivalence *s;

    HASH_FIND_INT( label_parents, &label, s);

    if(s==NULL){
        s = malloc(sizeof(struct label_equivalence));
        s->label = label;
        s->size = 50;
        s->parent = malloc(s->size * sizeof(int));
        s->count = 0;
        s->parent[s->count++] = parent_label;
        s->visited = 0;

        // printf("IN ADD: %lu", sizeof(s->parent)/sizeof(s->parent[0]));
        HASH_ADD_INT( label_parents, label, s );  /* id: name of key field */
    }
    if (s->size == s->count) {
        s->size *= 2;
        s->parent = realloc(s->parent, s->size * sizeof(int));
    }
    int i;
    for(i=0; i<s->count;i++){
        if(s->parent[i]==parent_label) break;
    }

    if(i==s->count) s->parent[s->count++] = parent_label;
}

struct label_equivalence *find_parent_label(int label) {
    struct label_equivalence *s;

    HASH_FIND_INT( label_parents, &label, s);  /* s: output pointer */
    return s;
}


/* A dictionary (KEY, VALUE) with 
- KEY: label
- VALUE: count of the corresponding label
*/

struct label_count {
    int label;                    /* key */
    int count;
    UT_hash_handle hh;         /* makes this structure hashable */
};

struct label_count *label_counts = NULL; // my label-count hashtable

void add_label_count(int label, int count) {
    struct label_count *s;

    HASH_FIND_INT( label_counts, &label, s);

    if(s == NULL){
        s = malloc(sizeof(struct label_count));
        s->label = label;
        s->count = count;
        HASH_ADD_INT( label_counts, label, s );  /* id: name of key field */
    }
    // If count exists, add 1 to the existing count
    s->count += count;
}

struct label_count *find_label_count(int label) {
    struct label_count *s;

    HASH_FIND_INT( label_counts, &label, s);  /* s: output pointer */
    return s;
}









// Function Prototype
Matrix labelImage(Image img);
int numberOfLetters(Matrix matrix, int threshold);

int main(int argc, const char * argv[]) {
	// Generate a random seed for random number generation
	srand(time(0));

    // Captcha image type 1 - ../CCLData/thresholded_sc_pbm_images/348.pbm
    // Captcha image type 2 - ../CCLData/thresholded_sc_pbm_images/348.pbm
	Image inputImage = readImage("../CCLData/thresholded_sc_pbm_images/348.pbm");

    clock_t t;
    t = clock();
    

	Matrix matrix = labelImage(inputImage);

    t = clock() - t;
    double time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
    printf("Time taken: %lf", time_taken);
    /*----------------- THRESHOLDING ----------------*/
    int threshold = 50;
    int n = numberOfLetters(matrix, threshold);
    int arr[n];
    int count = 0;

    struct label_count *lc;
    for(lc=label_counts; lc != NULL; lc=(struct label_count*)(lc->hh.next)) {
        if(lc->count > threshold){
            arr[count] = lc->label;
            count++;
        }
    }
    /*----------------- THRESHOLDING ----------------*/

    // Retrieve the maximum label in the matrix
    int maxLabel = 0;
    for(int i=0;i<matrix.height;i++){
        for(int j=0;j<matrix.width;j++){
            if(matrix.map[i][j] > maxLabel) maxLabel = matrix.map[i][j];
        }
    }

    // Prepare the "label: color" dictionary
    for(int i=1;i<=maxLabel;i++){
        add_label_color(i, rand()%255, rand()%255, rand()%255, rand()%255);
    }

    // Assign colors to pixels based on labels
    struct label_colors *m;
    for(int i=0;i<matrix.height;i++){
        for(int j=0;j<matrix.width;j++){
            // extra
            int flag = 0;
            for(int t=0;t<n;t++){
                if(arr[t] == (int)matrix.map[i][j]){
                    flag = 1;
                    break;
                }
            }
            if(flag==0){
                setPixel(inputImage, i, j, 255, 255, 255, 255);
            }
            if(matrix.map[i][j] != 255 && flag == 1){
                m = find_label_color((int)matrix.map[i][j]);
                if(m != NULL){
                    setPixel(inputImage, i, j, m->r, m->g, m->b, m->i);
                }
                
            }
        }
    }

    // Type 1 output - ../CCLData/colored_images/348.ppm
    // Type 2 output - ../CCLData/colored_images/0.ppm
    writeImage(inputImage, "../CCLData/colored_images/348.ppm");
	/* Delete the input image */
	deleteImage(inputImage);
	
	printf("Program ends ... ");

	return 0;
}

Matrix labelImage(Image img){
    Matrix matrix = image2Matrix(img);
    
    
    int counter = 1;
    for(int i=0;i<img.height;i++){
        for(int j=0;j<img.width;j++){
            // If white pixel, consider it as background and skip
            if(img.map[i][j].i == 255) continue;

            if(img.map[i][j].i == 0 && i!=0 && j!=0){

                // if pixel up and left are labelled and equal
                if(matrix.map[i][j-1] != 255 && matrix.map[i-1][j] != 255 && matrix.map[i-1][j] == matrix.map[i][j-1]){
                    matrix.map[i][j] = matrix.map[i-1][j];
                }

                // if only the left pixel is labelled
                if(matrix.map[i][j-1] != 255 && matrix.map[i-1][j] == 255){
                    matrix.map[i][j] = matrix.map[i][j-1];
                }
                
                // if only the up pixel is labelled
                else if(matrix.map[i-1][j] != 255 && matrix.map[i][j-1] == 255){
                    matrix.map[i][j] = matrix.map[i-1][j];
                }

                // If pixel up and left are different, the upper label is given to the current pixel.
                // Additionally these two pixel labels are remembered for further iteration as belonging to the same object.
                if(matrix.map[i][j-1] != 255 && matrix.map[i-1][j] != 255 && matrix.map[i-1][j] != matrix.map[i][j-1]){
                    matrix.map[i][j] = matrix.map[i-1][j];
                    add_parent_label(matrix.map[i][j-1], matrix.map[i][j]);
                }
                // If neither of them is labelled
                if(matrix.map[i][j-1] == 255 && matrix.map[i-1][j] == 255){
                    matrix.map[i][j] = counter;
                    counter++;

                }
                
            }
        }
    }

    /* SECOND ITERATION WITH EQUIVALENCE TABLE IMPLEMENTED VIA HASHTABLE */
    struct label_equivalence *le;
    for(int i=0;i<matrix.height;i++){
        for(int j=0;j<matrix.width;j++){
            if(matrix.map[i][j]!=255){
                
                double parent_label = matrix.map[i][j];
                double temp_label = parent_label;
                int min_parent;
                // printf("PIXEL: %d, %d: %lf\n", i, j, matrix.map[i][j]);
                while(1){
                    le = find_parent_label(parent_label);
                    if(le == NULL) break;
                    int min = 999999;
                    for(int k=0;k<le->count;k++){
                        if(le->parent[k]<min){
                            min = le->parent[k];
                            min_parent = min;
                        }
                    }
                    
                    if(min == temp_label) break;

                    temp_label = parent_label;
                    // printf("REACHED HERE\n");
                    parent_label = (double)min;
                    
                    
                }

                le = find_parent_label(matrix.map[i][j]);
                if(le!=NULL && le->count > 1){
                    for(int k=0;k<le->count;k++){
                        if(le->parent[k] != min_parent){
                            add_parent_label(le->parent[k], min_parent);
                        }
                    }
                }
                matrix.map[i][j] = parent_label;
            }
            
        }
    }

    return matrix;
}

int numberOfLetters(Matrix matrix, int threshold){
    struct label_count *lc;
    for(int i=0;i<matrix.height;i++){
        for(int j=0;j<matrix.width;j++){
            if(matrix.map[i][j] != 255){
                add_label_count(matrix.map[i][j], 1);
            }
        }
    }

    int n = 0;
    for(lc=label_counts; lc != NULL; lc=(struct label_count*)(lc->hh.next)) {
        if(lc->count > threshold){
            n++;
        }
    }
    printf("Number of Letters: %d\n", n);
    return n;
}