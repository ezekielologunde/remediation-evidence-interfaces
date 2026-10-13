permit (
    principal is User,
    action == Action::"View",
    resource is Document
)
when {
    principal in Role::"ClinicalResearcher" &&
    principal.clearanceLevel > 3 &&
    resource.classification != "HighlyRestricted" &&
    resource.projectStatus == "Active" &&
    principal.department == resource.projectManagingDepartment
};
permit (
    principal is User,
    action == Action::"View",
    resource is Document
)
when {
    principal in Role::"PrincipalInvestigator" &&
    context.networkRiskScore < 20 &&
    context.isCompliantDevice == true &&
    resource.projectStatus == "Active" &&
    principal.department == resource.projectManagingDepartment
};
permit (
    principal is User,
    action == Action::"Edit",
    resource is Document
)
when {
    principal in Role::"PrincipalInvestigator" &&
    context.networkRiskScore < 20 &&
    context.isCompliantDevice == true &&
    resource.projectStatus == "Active" &&
    principal.department == resource.projectManagingDepartment
};
permit (
    principal is User,
    action == Action::"Edit",
    resource is Document
)
when {
    principal in Role::"DataManager" &&
    principal.clearanceLevel > 5 &&
    resource.projectStatus == "Active" &&
    resource.classification == "HighlyRestricted" &&
    principal.department == resource.projectManagingDepartment
};
permit (
    principal is User,
    action == Action::"View",
    resource is Document
)
when {
    principal in Role::"GlobalAuditor" &&
    principal in Role::"ClinicalResearcher" &&
    principal.clearanceLevel > 3 &&
    resource.classification != "HighlyRestricted" &&
    resource.projectStatus == "Active" &&
    principal.department != resource.projectManagingDepartment
};