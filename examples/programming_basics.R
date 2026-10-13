# Run from the project root: Rscript examples/programming_basics.R
# Base R only; artificial values do not support biological conclusions.
measurements <- read.csv('examples/data/programming_measurements.csv',
                         na.strings = c('NA', ''), stringsAsFactors = FALSE,
                         colClasses = c(sample_id = 'character', value = 'character'))
metadata <- read.csv('examples/data/programming_metadata.csv', stringsAsFactors = FALSE,
                     colClasses = 'character')
stopifnot(all(c('sample_id','value') %in% names(measurements)),
          all(c('sample_id','condition','batch') %in% names(metadata)),
          !anyNA(measurements$sample_id), !anyNA(metadata$sample_id),
          all(nzchar(measurements$sample_id)), all(nzchar(metadata$sample_id)),
          !anyDuplicated(measurements$sample_id), !anyDuplicated(metadata$sample_id),
          setequal(measurements$sample_id, metadata$sample_id))
observed <- !is.na(measurements$value)
numeric_values <- suppressWarnings(as.numeric(measurements$value))
if (any(!is.finite(numeric_values[observed]))) {
  stop('Non-finite or invalid value; use NA for missing values')
}
measurements$value <- numeric_values
joined <- merge(measurements, metadata, by = 'sample_id', sort = FALSE)
joined <- joined[match(measurements$sample_id, joined$sample_id), ]
stopifnot(identical(joined$sample_id, measurements$sample_id))
joined$condition <- factor(joined$condition, levels = c('A', 'B'))
summary_table <- data.frame(
  condition = c('A', 'B'),
  n = sapply(c('A', 'B'), function(g) sum(!is.na(joined$value[joined$condition == g]))),
  mean = sapply(c('A', 'B'), function(g) mean(joined$value[joined$condition == g], na.rm = TRUE)))
fit <- lm(value ~ condition, data = joined, na.action = na.exclude)
stopifnot(nrow(joined) == 8, sum(is.na(joined$value)) == 1,
          identical(as.numeric(summary_table$n), c(3,4)),
          isTRUE(all.equal(as.numeric(summary_table$mean), c(2,5.5))),
          abs(unname(coef(fit)[['conditionB']]) - 3.5) < 1e-12)
output_dir <- 'examples/output/programming/r'
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
write.csv(joined, file.path(output_dir, 'joined.csv'), row.names = FALSE, na = 'NA')
write.csv(summary_table, file.path(output_dir, 'summary.csv'), row.names = FALSE)
writeLines(capture.output(sessionInfo()), file.path(output_dir, 'session-info.txt'))
pdf(file.path(output_dir, 'values.pdf'), width = 5, height = 3.5, family = 'Courier')
par(mar = c(4, 4, 3, 1), cex = 0.8)
plot(value ~ condition, data = joined, xlab = 'Artificial condition', ylab = 'Artificial value',
     main = 'Artificial values by condition')
set.seed(20261013)
stripchart(value ~ condition, data = joined, vertical = TRUE, method = 'jitter', add = TRUE, pch = 19)
dev.off()
print(summary_table)
print(coef(fit))
