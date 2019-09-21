library(cluster)
library(dplyr)
library(ggplot2)
library(readr)
library(Rtsne)

video = read.csv("path-to-file", header=T)
video_gb = data.frame(video$Platform,video$Genre,video$Critic_Score,video$Rating,video$Global_Sales)
video_na = data.frame(video$Platform,video$Genre,video$Critic_Score,video$Rating,video$NA_Sales)
video_eu = data.frame(video$Platform,video$Genre,video$Critic_Score,video$Rating,video$EU_Sales)
video_jp = data.frame(video$Platform,video$Genre,video$Critic_Score,video$Rating,video$JP_Sales)
video_ot = data.frame(video$Platform,video$Genre,video$Critic_Score,video$Rating,video$Other_Sales)

gb_gower_dist <- daisy(video_gb, metric = "gower")
gb_gower_mat <- as.matrix(video_gb)

na_gower_dist <- daisy(video_na, metric = "gower")
na_gower_mat <- as.matrix(video_na)

eu_gower_dist <- daisy(video_eu, metric = "gower")
eu_gower_mat <- as.matrix(video_eu)

jp_gower_dist <- daisy(video_jp, metric = "gower")
jp_gower_mat <- as.matrix(video_jp)

ot_gower_dist <- daisy(video_ot, metric = "gower")
ot_gower_mat <- as.matrix(video_ot)


#Global Clustering
gb_sil_width <- c(NA)
for(i in 2:8){  
  gb_pam_fit <- pam(gb_gower_dist, diss = TRUE, k = i)  
  gb_sil_width[i] <- gb_pam_fit$silinfo$avg.width  
}
plot(1:8, gb_sil_width,
     xlab = "Number of clusters",
     ylab = "Silhouette Width")
lines(1:8, gb_sil_width)

k <- 5
gb_pam_fit <- pam(gb_gower_dist, diss = TRUE, k)
gb_pam_results <- video_gb %>%
  mutate(cluster = gb_pam_fit$clustering) %>%
  group_by(cluster) %>%
  do(the_summary = summary(.))
gb_pam_results$the_summary

video_gb$cluster = gb_pam_fit$clustering

gb_tsne_obj <- Rtsne(gb_gower_dist, is_distance = TRUE)
gb_tsne_data <- gb_tsne_obj$Y %>%
  data.frame() %>%
  setNames(c("X", "Y")) %>%
  mutate(cluster = factor(gb_pam_fit$clustering))
ggplot(aes(x = X, y = Y), data = gb_tsne_data) +
  geom_point(aes(color = cluster))


#NA Clustering
na_sil_width <- c(NA)
for(i in 2:8){  
  na_pam_fit <- pam(na_gower_dist, diss = TRUE, k = i)  
  na_sil_width[i] <- na_pam_fit$silinfo$avg.width  
}
plot(1:8, na_sil_width,
     xlab = "Number of clusters",
     ylab = "Silhouette Width")
lines(1:8, na_sil_width)

k <- 5
na_pam_fit <- pam(na_gower_dist, diss = TRUE, k)
na_pam_results <- video_na %>%
  mutate(cluster = na_pam_fit$clustering) %>%
  group_by(cluster) %>%
  do(the_summary = summary(.))
na_pam_results$the_summary

video_na$cluster = na_pam_fit$clustering

na_tsne_obj <- Rtsne(na_gower_dist, is_distance = TRUE)
na_tsne_data <- na_tsne_obj$Y %>%
  data.frame() %>%
  setNames(c("X", "Y")) %>%
  mutate(cluster = factor(na_pam_fit$clustering))
ggplot(aes(x = X, y = Y), data = na_tsne_data) +
  geom_point(aes(color = cluster))


#EU Clustering
eu_sil_width <- c(NA)
for(i in 2:8){  
  eu_pam_fit <- pam(eu_gower_dist, diss = TRUE, k = i)  
  eu_sil_width[i] <- eu_pam_fit$silinfo$avg.width  
}
plot(1:8, eu_sil_width,
     xlab = "Number of clusters",
     ylab = "Silhouette Width")
lines(1:8, eu_sil_width)

k <- 5
eu_pam_fit <- pam(eu_gower_dist, diss = TRUE, k)
eu_pam_results <- video_eu %>%
  mutate(cluster = eu_pam_fit$clustering) %>%
  group_by(cluster) %>%
  do(the_summary = summary(.))
eu_pam_results$the_summary

video_eu$cluster = eu_pam_fit$clustering

eu_tsne_obj <- Rtsne(eu_gower_dist, is_distance = TRUE)
eu_tsne_data <- eu_tsne_obj$Y %>%
  data.frame() %>%
  setNames(c("X", "Y")) %>%
  mutate(cluster = factor(eu_pam_fit$clustering))
ggplot(aes(x = X, y = Y), data = eu_tsne_data) +
  geom_point(aes(color = cluster))


#JP Clustering
jp_sil_width <- c(NA)
for(i in 2:8){  
  jp_pam_fit <- pam(jp_gower_dist, diss = TRUE, k = i)  
  jp_sil_width[i] <- jp_pam_fit$silinfo$avg.width  
}
plot(1:8, jp_sil_width,
     xlab = "Number of clusters",
     ylab = "Silhouette Width")
lines(1:8, jp_sil_width)

k <- 5
jp_pam_fit <- pam(jp_gower_dist, diss = TRUE, k)
jp_pam_results <- video_jp %>%
  mutate(cluster = jp_pam_fit$clustering) %>%
  group_by(cluster) %>%
  do(the_summary = summary(.))
jp_pam_results$the_summary

video_jp$cluster = jp_pam_fit$clustering

jp_tsne_obj <- Rtsne(jp_gower_dist, is_distance = TRUE)
jp_tsne_data <- jp_tsne_obj$Y %>%
  data.frame() %>%
  setNames(c("X", "Y")) %>%
  mutate(cluster = factor(jp_pam_fit$clustering))
ggplot(aes(x = X, y = Y), data = jp_tsne_data) +
  geom_point(aes(color = cluster))


#Other Clustering
ot_sil_width <- c(NA)
for(i in 2:8){  
  ot_pam_fit <- pam(ot_gower_dist, diss = TRUE, k = i)  
  ot_sil_width[i] <- ot_pam_fit$silinfo$avg.width  
}
plot(1:8, ot_sil_width,
     xlab = "Number of clusters",
     ylab = "Silhouette Width")
lines(1:8, ot_sil_width)

k <- 5
ot_pam_fit <- pam(ot_gower_dist, diss = TRUE, k)
ot_pam_results <- video_ot %>%
  mutate(cluster = ot_pam_fit$clustering) %>%
  group_by(cluster) %>%
  do(the_summary = summary(.))
ot_pam_results$the_summary

video_ot$cluster = ot_pam_fit$clustering

ot_tsne_obj <- Rtsne(ot_gower_dist, is_distance = TRUE)
ot_tsne_data <- ot_tsne_obj$Y %>%
  data.frame() %>%
  setNames(c("X", "Y")) %>%
  mutate(cluster = factor(ot_pam_fit$clustering))
ggplot(aes(x = X, y = Y), data = ot_tsne_data) +
  geom_point(aes(color = cluster))




