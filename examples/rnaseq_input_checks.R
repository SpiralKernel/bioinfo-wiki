# Shared input checks for the native-R teaching case; no package dependencies.
align_rnaseq_inputs <- function(counts, samples) {
  if (!is.matrix(counts) || !is.numeric(counts) || !nrow(counts) || !ncol(counts)) stop('counts must be a nonempty numeric matrix')
  if (is.null(rownames(counts)) || anyNA(rownames(counts)) || any(!nzchar(rownames(counts))) || anyDuplicated(rownames(counts))) stop('duplicate or missing gene IDs')
  if (is.null(colnames(counts)) || anyNA(colnames(counts)) || any(!nzchar(colnames(counts))) || anyDuplicated(colnames(counts))) stop('duplicate or missing count sample IDs')
  if (!is.data.frame(samples) || !'sample_id' %in% names(samples)) stop('samples needs sample_id')
  ids <- as.character(samples$sample_id)
  if (anyNA(ids) || any(!nzchar(ids)) || anyDuplicated(ids)) stop('duplicate or missing metadata sample IDs')
  if (!setequal(colnames(counts), ids)) stop('count/metadata sample sets differ')
  if (anyNA(counts) || any(!is.finite(counts)) || any(counts < 0) || any(counts != floor(counts))) stop('counts must be finite nonnegative integers, not TPM')
  if (any(colSums(counts) == 0)) stop('empty count library')
  samples <- samples[match(colnames(counts), ids), , drop=FALSE]
  rownames(samples) <- samples$sample_id
  stopifnot(identical(colnames(counts), rownames(samples)))
  list(counts=counts, samples=samples)
}
check_rnaseq_design <- function(samples, formula) {
  variables <- all.vars(formula)
  if (!all(variables %in% names(samples)) || anyNA(samples[, variables, drop=FALSE])) stop('missing design variables')
  matrix <- model.matrix(formula, samples)
  if (qr(matrix)$rank < ncol(matrix)) stop('design is not full rank: confounding or redundant terms')
  if (nrow(matrix) <= ncol(matrix)) stop('no residual degrees of freedom')
  matrix
}
