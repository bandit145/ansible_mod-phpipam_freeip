param(
    [string]$PHPIPamPath
)

$env:phpipam_path = $PHPIPamPath

vagrant up --provision