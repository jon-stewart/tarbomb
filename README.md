# tartool

Build tarbomb using streams.

Ensures that absolute file paths are used in the TAR header blocks.  Python tarfile library will not strip the path information giving us arbitrary file write.
