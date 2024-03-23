# SR-TE-by-PLL
Segment Routing Traffic Engineering by Pruned Landmark Label



Abstract
As network usage is increasing recently, providers are faced with the dual challenge of enhancing network performance while also optimizing link utilization. In a provider’s network with a redundant structure, there may be multiple shortest routes. However, basic route control typically selects only one of these paths, leading to potential link congestion. For this reason, Traffic Engineering (TE) utilizing Multi-Protocol Label Switching (MPLS) and Segment Routing (SR) have been developed to enable the selection of routes other than the shortest path. Despite the various methods that have been proposed, the challenge of selecting the optimal route has not yet been resolved. In this paper, we focus on Segment Routing Traffic Engineering (SR-TE) in Software-Defined Networking (SDN) networks. We propose a heuristic Pruned Landmark Labeling (hPLL) method that dynamically selects the best Landmark as the intermediate node for each traffic flow. This reduces the Maximum Link Utilization (MLU) in the network with restricted Segment Identifiers (SIDs), making it more suitable for large-scale SR operator networks. Through a series of experiments, we demonstrate that our proposed algorithm outperforms traditional routing algorithms to a significant extent. 

Index Terms—Traffic Engineering, Segment Routing, Pruned Landmark Labeling
