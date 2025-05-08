# Holistic molecular descriptors for scaffold hopping

Weighted Holistic Atom Localization and Entity Shape (WHALES) is a descriptors based on 3D structure to facilitate natural product featurization. It is aimed at scaffold hopping exercises from natural products to synthetic compounds

This model was incorporated on 2021-07-15.

## Information
### Identifiers
- **Ersilia Identifier:** `eos3ae6`
- **Slug:** `whales-descriptor`

### Domain
- **Task:** `Representation`
- **Subtask:** `Featurization`
- **Biomedical Area:** `Any`
- **Target Organism:** `Not Applicable`
- **Tags:** `Natural product`, `Descriptor`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `33`
- **Output Consistency:** `Fixed`
- **Interpretation:** Vector representation of a molecule

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| r_00 | float |  | WHALES descriptor remoteness (R) 0  |
| r_01 | float |  | WHALES descriptor remoteness (R) 1  |
| r_02 | float |  | WHALES descriptor remoteness (R) 2  |
| r_03 | float |  | WHALES descriptor remoteness (R) 3  |
| r_04 | float |  | WHALES descriptor remoteness (R) 4  |
| r_05 | float |  | WHALES descriptor remoteness (R) 5  |
| r_06 | float |  | WHALES descriptor remoteness (R) 6  |
| r_07 | float |  | WHALES descriptor remoteness (R) 7  |
| r_08 | float |  | WHALES descriptor remoteness (R) 8  |
| r_09 | float |  | WHALES descriptor remoteness (R) 9  |

_10 of 33 columns are shown_
### Source and Deployment
- **Source:** `Local`
- **Source Type:** `External`
- **DockerHub**: [https://hub.docker.com/r/ersiliaos/eos3ae6](https://hub.docker.com/r/ersiliaos/eos3ae6)
- **Docker Architecture:** `AMD64`, `ARM64`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos3ae6.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos3ae6.zip)

### Resource Consumption
- **Model Size (Mb):** `1`
- **Environment Size (Mb):** `508`
- **Image Size (Mb):** `454.41`


### References
- **Source Code**: [https://github.com/ETHmodlab/scaffold_hopping_whales](https://github.com/ETHmodlab/scaffold_hopping_whales)
- **Publication**: [https://www.nature.com/articles/s42004-018-0043-x](https://www.nature.com/articles/s42004-018-0043-x)
- **Publication Type:** `Peer reviewed`
- **Publication Year:** `2018`
- **Ersilia Contributor:** [miquelduranfrigola](https://github.com/miquelduranfrigola)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [MIT](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos3ae6
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos3ae6
# generate an example file
ersilia example -n 3 -f my_input.csv
# run the model
ersilia run -i my_input.csv -o my_output.csv
# close the model
ersilia close
```

## About Ersilia
The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit organization fueling sustainable research in the Global South.
Please [cite](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff) the Ersilia Model Hub if you've found this model to be useful. Always [let us know](https://github.com/ersilia-os/ersilia/issues) if you experience any issues while trying to run it.
If you want to contribute to our mission, consider [donating](https://www.ersilia.io/donate) to Ersilia!
