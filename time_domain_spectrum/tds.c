#include<stdio.h>
#include<stdlib.h>
#include<math.h>

#define true 1
#define false 0
#define MAXCHAR 1000
#define len(vector, type) ((int)sizeof(vector)/(sizeof(type)))

float* read_data(char* filename, int *size)
{
    FILE *fp;
    fp = fopen(filename,"r");
    char len_str[10];
    fgets(len_str, 10, fp);
    int len = atoi(len_str);
    *size = len;
    float *data = (float*) malloc(len*sizeof(float));
    char *row = (char*) malloc(MAXCHAR*sizeof(char));
    int i = 0;
    while (feof(fp) != true && i < len)
    {
        fgets(row, MAXCHAR, fp);
        data[i] = atof(row);
        i++;
    }

    return data;
}

int main(int argc, char *argv[])
{
    char filename[] = "data.csv";
    int N;
    float *data = read_data(filename, &N);
    printf("Tamanho vetor: %d\n", N);
    int i = 0;
    for (i; i < N; i++)
    {
        printf("%f", data[i]);
        printf("\n");
    }
    return 0;
}