# UmbraRepository-Unstable-Testing
Package repository for testing

Repository Architecture:
```
UmbraRepository-Unstable-Testing/
├── index.json        # Primary catalog metadata file consumed by the package manager
├── package1/         # Packaged binaries, libraries for package1
│   └── package1.tar.gz
└── package2/         # Packaged binaries, libraries for package2
    └── package2.tar.gz
```
Index.json structure:
```
{
  "package1": {
    "latest": "1.0.0",
    "versions": {
      "1.0.0": "package1/package1-1.0.0.tar.gz"
    }
  }
}
```
