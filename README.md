# CETONI SiLA 2 Motioncontrol SDK
## Installation
Run `pip install .` from the root directory containing the file `setup.py`

## Usage
Run `python -m sila_cetoni_motioncontrol --help` to receive a full list of available options

## Code generation
- generate
  ```console
  $ python -m sila2.code_generator new-package -n axis_service -o ./sila_cetoni/motioncontrol/axis/sila ./sila_cetoni/motioncontrol/axis/features*.sila.xml
  ```
- update
  ```console
  $ python -m sila2.code_generator update -d ./sila_cetoni/motioncontrol/axis/sila ./sila_cetoni/motioncontrol/axis/features*.sila.xml
  ```
