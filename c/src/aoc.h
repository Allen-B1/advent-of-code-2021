#ifndef _AOC_H
#define _AOC_H
#include <curl/curl.h>
#include <stdio.h>
#include <string.h>
#include <inttypes.h>
#include <stdlib.h>
#include <stdbool.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>

static char AOC_SESSION[512];

struct AocState {
    CURL* curl;
};

struct AocState state;

typedef struct {
    int year;
    int day;
} AocLevel;

__attribute__((constructor))
static void aoc_init() {
    state.curl = curl_easy_init();
    const char* sessionptr = getenv("AOC_SESSION");
    if (sessionptr == NULL) {
        fprintf(stderr, "$AOC_SESSION not set");
        exit(1);
    }
    strcpy(AOC_SESSION, sessionptr);
}

typedef struct {
    size_t size;
    char* data;
} _AocBuf;

size_t aoc_write_data(void *buffer, size_t size, size_t nmemb, void *userp) {
    if (size*nmemb > ((_AocBuf*)userp)->size - 1) 
        return -1;
    memcpy(((_AocBuf*)userp)->data, buffer, size*nmemb);
    ((_AocBuf*)userp)->size = size*nmemb;
    ((_AocBuf*)userp)->data[size*nmemb] = '\0';
    return size*nmemb;
}

static ssize_t aoc_fetch(AocLevel level, char* out_buf, size_t size) {
    static char buf[256];
    memset(buf, 0, 256);
    snprintf(buf, 255, "https://adventofcode.com/%d/day/%d/input", level.year, level.day);
    curl_easy_setopt(state.curl, CURLOPT_URL, buf);

    static char sessionbuf[512];
    memset(sessionbuf, 0, 512);
    snprintf(sessionbuf, 511, "session=%s", AOC_SESSION);
    curl_easy_setopt(state.curl, CURLOPT_COOKIE, sessionbuf);

    curl_easy_setopt(state.curl, CURLOPT_WRITEFUNCTION, aoc_write_data);
    _AocBuf outbuf;
    outbuf.size = size;
    outbuf.data = out_buf;
    curl_easy_setopt(state.curl, CURLOPT_WRITEDATA, &outbuf);

    char err_buf[CURL_ERROR_SIZE];
    /* provide a buffer to store errors in */
    curl_easy_setopt(state.curl, CURLOPT_ERRORBUFFER, err_buf);

    CURLcode code = curl_easy_perform(state.curl);
    if (code != CURLE_OK) {
        fprintf(stderr, "%s\n", err_buf);
        return -1;
    }
    return outbuf.size;
}

static ssize_t aoc_fetchc(AocLevel level, char* outbuf, size_t size) {
    static char path[256] = {0};
    snprintf(path, 255, ".cache/%d-%d.txt", level.year, level.day);

    if (access(path, F_OK) == 0) {
        // file cached
        int f = open(path, O_RDONLY);
        int size = read(f, outbuf, size);
        if (size < 0) {
            return -1;
        }
        close(f);
        return size;
    } else {
        ssize_t size = aoc_fetch(level, outbuf, size);
        if (size < 0) {
            return -1;
        }

        int f = creat(path, S_IRUSR | S_IWUSR  | S_IRGRP  | S_IWGRP |S_IROTH);
        puts(path);
        write(f, outbuf, size);
        close(f);
        return size;
    }
}

static void aoc_debug(AocLevel level, int64_t (*func)(const char* inp), const char* test_inp, int64_t test_out) {
    int64_t test_out_res = func(test_inp);
    printf("Test Output: %" PRId64 "\n", test_out_res);
    if (test_out_res != test_out) {
        printf("Incorrect!\n");
        return;
    }

    static char real_inp[65536];
    aoc_fetchc(level, real_inp, sizeof(real_inp));

    int64_t real_out = func(real_inp);
    printf("Real Output: %" PRId64 "\n", real_out);
}

__attribute__((destructor))
static void aoc_deinit() {
    curl_easy_cleanup(state.curl);
}

#endif