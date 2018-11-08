# Getting started

Get instructions with

```bash
ct --help
```


### Create a Confluence page with page properties only

For creating a page with page properties only you can run a command like:

```bash
ct page-prop-set \
   -l "first-label" -l "second-label" \
   -p "SPACE:parent page title" \
   "IT:new page titile" \
   "Property:=value" \
   "Name:=some name"
```

### Get confluence profile data for a user

```bash
ct get --stream /display/~user
```

### Get page properties of only approved pages (with Comala Workflow)

```bash
ct page-prop-get 'label = "first-label"' --dict -s Approved
```

### Automatically change a state (comala workflow)

```bash
ct cw approve -n "Approval Name" "SPACE:Page title"
```

### Reject a page
```bash
ct cw reject -m - -n "Approval Name" "SPACE:Page title" <<!
Some message
!
```

  
Documentation with pydoc-markdown (and mkdocs)
