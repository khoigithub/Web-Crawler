# Image Build Locations

To help keep track of which CI pushes which image where. The order of 'built by' matches the builder for apps-jenkins and nexus, respectively.

|     |                |
| --- | -------------- |
| GHA | Github Actions |
| J2  | Jenkins2       |

| Path                                                              | Built By | apps-jenkins                   | nexus               |
| ----------------------------------------------------------------- | -------- | ------------------------------ | ------------------- |
| [alpine](alpine/Dockerfile)                                       | , GHA    |                                | build-ccsmp-alpine  |
| [build-ccsmp-ol8-x68](build-ccsmp-ol8-x68/Dockerfile)             |          |                                |                     |
| [ccsmp-build-ce7-x86_64](ccsmp-build-ce7-x86_64/Dockerfile)       | J2       | ccsmp-build-ce7-x86_64         |                     |
| [ccsmp-musl](ccsmp-musl/Dockerfile)                               | J2       | build-ccsmp-musl               |                     |
| [ccsmp-ol8-arm64v8](ccsmp-ol8-arm64v8/Dockerfile)                 | J2       | ccsmp-ol8-arm64v8-test         |                     |
| [ccsmp-ce7-arm64v8](ccsmp-ce7-arm64v8/Dockerfile)                 | J2       | ccsmp-ce7-arm64v8              |                     |
| [centos8-x86_64-cross-arm](./centos8-x86_64-cross-arm/Dockerfile) | J2       | ccsmp-centos8-x86_64-cross-arm |                     |
| [oraclelinux-8-x86](./oraclelinux-8-x86/Dockerfile)               | J2, GHA  | build-ccsmp-ol8-x86            | build-ccsmp-ol8-x68 |
