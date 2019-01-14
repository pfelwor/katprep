# uyuni-basic

This cookbook deploys a [Uyuni](https://www.uyuni-project.org) server on openSUSE 42.3. For this, it will add the required software sources, install the packages and deploys the database. It also creates an initial organization and an admin account.
For the future, additional platforms and features might be supported. Feel free to let me know, what you're missing.

## Requirements
### Platforms
- openSUSE 42.3 (*no other platforms are currently supported for hosting Uyuni*)

## Attributes
The attributes used by this cookbook are under the ``uyuni`` namespace.

Attribute  | Description | Type | Default
---------- | ----------- | ---- | -------
admin_user | Uyuni admin username | String | vagrant
admin_pass | Uyuni admin password | String | vagrant
admin_mail | Uyuni admin mail address | String | uyuni@vagrantup.com
admin_name | Uyuni admin first name | String | Arthur
admin_surname | Uyuni admin surname | String | Admin
org_name | Uyuni organization name | String | Vagrant
db_name | Database name | String | uyuni
db_username | Database username | String | uyuni
db_password | Database password | String | SUSEManager1337
cert_city | SSL certificate city | String | Default City
cert_state | SSL certificate state | String | Default State
cert_country | SSL certificate country | String | DE
cert_mail | SSL certificate mail address | String | uyuni@vagrantup.com
cert_pass | SSL certificate password | String | vagrant
cert_ou | SSL certificate organzation unit | String | Default Organization

## Recipes
This section describes the recipes in the cookbook and how to use them in your environment.

### default
This recipe is an entry point and triggers additional recipes.

### packages
This recipe:
- ensures that the system is up2date
- configures the Uyuni server software repository
- installs the Uyuni server pattern

### uyuni
This recipe:
- creates an environment file
- deploys Uyuni via the installation utility
- creates an admin user and an initial organization
