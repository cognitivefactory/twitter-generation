# 📚 Data Loader

Because models take a minimum of 30GB of vRAM by default, loading additional data for generation can be quite the hassle. Because of (bad) hardware restrictions, dynamically loading data for generation is the way to go.

```c
__host__ ​ __device__ ​cudaError_t cudaMalloc ( void** devPtr, size_t size )
__host__             ​cudaError_t cudaMemcpy ( void* dst, const void* src, size_t count, cudaMemcpyKind kind )
__host__ ​ __device__ ​cudaError_t cudaFree   ( void* devPtr )
```

The life of data in a deep learning model is often the following:

1. loading the data with CPU into RAM (`malloc`)
2. allocating similar memory size into GPU vRAM (`cudaMalloc`)
3. copying data from RAM to vRAM (`cudaMemcpy`)
4. computing in GPU
5. copying data from vRAM to RAM
6. freeing data

Bullet points `2` and `3` are the critical parts in our system ; which means there is a need for reusing previously allocated memory or explicitly freeing it _after each request_ so that we fix the 143 error code or the 0x8007000e exception. Dynamically loading assets with python can be done with `Generator`s (amongst other wonderful alternatives). Because of the (very very) high level python interface of CUDA, memory management can not be done properly, which means we need a way to tell the pytorch interface to not cache any assets coming into the GPU vRAM. That is often done with the `.no_grad` context or decorator.

Because we may potentially load very large files into GPU vRAM for generation, this kind of loading method is required.

```py
is_whitespace = re.compile(r"\s+").match


class SomethingGenerator:
    def __init__(self, filepath: str) -> None:
        self.__path = filepath

    def __iter__(self) -> Generator[str, None, None]:
        with open(self.__path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not is_whitespace(line):
                    yield line
```

The downsides may include :

- keeping the inputs files opened for too long
- different RAM/vRAM managements strategies from the MMU which further slows multiple loadings
